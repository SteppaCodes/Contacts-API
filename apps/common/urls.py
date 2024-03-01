from django.urls import path
from django.shortcuts import redirect

from .views import RedirectVIew

urlpatterns = [
    path("", RedirectVIew.as_view()), 
    path("api", RedirectVIew.as_view())
    ]
