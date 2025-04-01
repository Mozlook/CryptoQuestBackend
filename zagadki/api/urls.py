from django.urls import path, include
from .views import sprawdz_zagadke

urlpatterns = [
    path('sprawdz/', sprawdz_zagadke, name='sprawdz_zagadke'),
]
