from django.urls import include, path

from .views import (BledyList, LoginView, SprawdzOdpowiedz, SprawdzProgres,
                    get_csrf_token, registration_view)

urlpatterns = [
    path("bledy/", BledyList.as_view(), name="BledyList"),
    path("get-csrf/", get_csrf_token, name="get_csrf"),
    path("register/", registration_view, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("sprawdz-progres/", SprawdzProgres.as_view(), name="sprawdz-progres"),
    path("sprawdz-odpowiedz/", SprawdzOdpowiedz.as_view(), name="sprawdz-odpowiedz"),
]
