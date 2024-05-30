from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Material(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=150)
    cost = models.FloatField(max_length=255)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='materials', verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('material-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title


class FlatCategory(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('material-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title
