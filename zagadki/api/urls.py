from django.urls import path, include
from .views import sprawdz_zagadke, BledyList

urlpatterns = [
    path('sprawdz/', sprawdz_zagadke, name='sprawdz_zagadke'),
    path('bledy/', BledyList.as_view(), name='BledyList'),
]
