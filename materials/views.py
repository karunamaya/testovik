from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import Category, Material
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CategorySerializer, MaterialSerializer, FlatCategorySerializer
from utils.excelParser import parser


class CategoryTreeView(APIView):
    def get(self, request):
        root_categories = Category.objects.root_nodes()
        serializer = CategorySerializer(root_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        materials = Material.objects.filter(category=request.data["parent"])
        if len(materials) > 0:
            return Response("Нельзя добавить категорию - это крайняя категория!",
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data=request.data)
        new_category = Category(title=request.data["title"], slug=request.data["slug"],
                                parent=Category(id=request.data["parent"]))

        if serializer.is_valid():
            new_category.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            categories = Category.objects.filter(id=request.data["id"])
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Failed to Update'}, safe=True)

        if len(categories) > 0:
            category = categories[0]
        else:
            return JsonResponse({'message': 'Material not found'}, status=404)
        category_serializer = CategorySerializer(category, data=request.data)
        print(category_serializer)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse({'message': 'Updated Successfully'}, safe=True)
        return JsonResponse({'message': 'Failed to Update'}, safe=True)

    def delete(self, request):
        try:
            category = Category.objects.get(id=request.data["id"])
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found'}, status=404)
        Material.objects.filter(category=category).delete()
        category.delete()

        return JsonResponse("Deleted Successfully", safe=False)


class MaterialView(APIView):
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request):
        category = Category.objects.filter(id=request.data["category"])
        serializer = CategorySerializer(category)
        children = []
        for cat in category:
            children = cat.children.all()
        if len(children) > 0:
            return Response("Нельзя добавить метериал - это не крайняя категория!",
                            status=status.HTTP_400_BAD_REQUEST)
        material_serializer = MaterialSerializer(data=request.data)
        if material_serializer.is_valid():
            material_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return Response("Проверьте правильность данных!",
                        status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        materials = Material.objects.filter(id=request.data["id"])
        material = materials[0]
        material_serializer = MaterialSerializer(material, data=request.data)
        if material_serializer.is_valid():
            material_serializer.save()
            return JsonResponse({'message': 'Updated Successfully'}, safe=True)
        print(material_serializer.errors)
        return JsonResponse({'message': 'Failed to Update'}, safe=True)

    def delete(self, request):
        try:
            material = Material.objects.get(id=request.data["id"])
        except Material.DoesNotExist:
            return JsonResponse({'message': 'Material not found'}, status=404)
        material.delete()
        return JsonResponse("Deleted Successfully", safe=False)


class CategoryFlatView(APIView):
    def get(self, request):
        serializer = FlatCategorySerializer(Category.objects.all())
        return Response(serializer.data)


@csrf_exempt
def excelApi(request, id=0):
    print(request)
    if request.method == 'POST':
        parser()
        return JsonResponse("Failejjd to Add", safe=False)
