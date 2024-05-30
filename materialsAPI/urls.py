from django.contrib import admin
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from materials.serializers import MaterialsAPI
from materials.views import CategoryTreeView, MaterialView, CategoryFlatView
from materials import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryTreeView.as_view()),
    path('flatcategories/', CategoryFlatView.as_view()),
    path('categories/create/', CategoryTreeView.as_view()),
    path('api/category/update', CategoryTreeView.as_view()),
    path('api/category/delete', CategoryTreeView.as_view()),
    path('materials/', MaterialView.as_view()),
    path('api/materials/update', MaterialView.as_view()),
    path('api/materials/delete', MaterialView.as_view()),
    re_path("api/excel", views.excelApi),

]

urlpatterns = format_suffix_patterns(urlpatterns)
