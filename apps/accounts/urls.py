from django.urls import path, include

from .views import (
    RegisterView, 
    LoginVIew,
    VerifyOTPAPIView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginVIew.as_view()),

    path("verify-email/", VerifyOTPAPIView.as_view())
]