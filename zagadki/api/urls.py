from django.urls import path, include
from .views import sprawdz_zagadke, BledyList, get_csrf_token, registration_view, LoginView

urlpatterns = [
    path('sprawdz/', sprawdz_zagadke, name='sprawdz_zagadke'),
    path('bledy/', BledyList.as_view(), name='BledyList'),
    path('get-csrf/', get_csrf_token, name='get_csrf'),
    path('register/', registration_view, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
]
