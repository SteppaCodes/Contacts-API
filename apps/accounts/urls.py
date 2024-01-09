from django.urls import path

from .views import (
    RegisterView, LoginVIew
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginVIew.as_view()),
]