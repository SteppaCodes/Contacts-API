from django.urls import path

from . views import ContactListCreateAPIView

urlpatterns = [
    path("contact-list/", ContactListCreateAPIView.as_view()),
    #path("contact-list/", ContactListAPIView.as_view()),
]