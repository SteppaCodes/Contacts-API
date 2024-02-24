from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView, 
    LoginVIew,
    VerifyOTPAPIView,
    LogoutAPIView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginVIew.as_view()),
    path("logout/", LogoutAPIView.as_view()),

    path("verify-email/", VerifyOTPAPIView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]