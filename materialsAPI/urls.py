from django.contrib import admin
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from materials.serializers import MaterialsAPI
from materials.views import CategoryTreeView, MaterialView, CategoryFlatView
from materials import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categories/', CategoryTreeView.as_view()),
    path('api/flatcategories/', CategoryFlatView.as_view()),
    path('api/materials/', MaterialView.as_view()),
    re_path("api/excel/", views.excelApi),
]

urlpatterns = format_suffix_patterns(urlpatterns)
