from django.urls import path

from . views import ContactListAPIView

urlpatterns = [
    path("contact-list/", ContactListAPIView.as_view()),
    #path("contact-list/", ContactListAPIView.as_view()),
]