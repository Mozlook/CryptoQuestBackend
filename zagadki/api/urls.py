from django.urls import path, include
from .views import BledyList, get_csrf_token, registration_view, LoginView, SprawdzProgres

urlpatterns = [
    path('bledy/', BledyList.as_view(), name='BledyList'),
    path('get-csrf/', get_csrf_token, name='get_csrf'),
    path('register/', registration_view, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/sprawdz-progres/', SprawdzProgres.as_view(), name='sprawdz-progress'),

    
]
