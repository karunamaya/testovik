from rest_framework import serializers, generics

from .models import Category, Material


class MaterialSerializerByCategory(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['title', 'cost']  # '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["id","title", "slug", "cost", "category"]  # '__all__'


class MaterialsAPI(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    summa = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['summa', 'id', 'title', 'slug', 'children', 'materials']

    def get_children(self, obj):
        if obj.is_leaf_node():
            return []
        return CategorySerializer(obj.get_children(), many=True).data

    def get_materials(self, obj):
        # if obj.is_leaf_node():
        return MaterialSerializerByCategory(obj.materials.all(), many=True).data
        # return []

    def get_summa(self, obj):
        if obj.materials.exists():
            return sum(material.cost for material in obj.materials.all())
        elif obj.children.exists():
            summa = 0
            for child in obj.children.all():
                summa += self.get_summa(child)
            return summa
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['children']:
            del representation['children']
        if not representation['materials']:
            del representation['materials']
        return representation


class FlatCategorySerializer(serializers.ModelSerializer):
    categories = serializers.ListField(child=serializers.DictField())

    def to_representation(self, instance):
        categories = []
        processed_categories = set()

        def traverse(categories_queryset):
            for category in categories_queryset:
                if category.id in processed_categories:
                    continue
                processed_categories.add(category.id)
                materials = category.materials.all()
                materials_list = [{'id': material.id, 'title': material.title, 'cost': material.cost} for material in materials]
                category_dict = {'id': category.id, 'title': category.title, 'slug': category.slug,
                                 'parent_id': category.parent_id}
                if materials_list:
                    category_dict['materials'] = materials_list
                categories.append(category_dict)
                if hasattr(category, 'children') and category.children.exists():
                    traverse(category.children.all())

        traverse(Category.objects.all())
        return {'categories': categories}
