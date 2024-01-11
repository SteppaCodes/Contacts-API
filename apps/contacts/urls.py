from django.urls import path

from . views import ContactListCreateAPIView, ContactDetailView

urlpatterns = [
    path("contact-list/", ContactListCreateAPIView.as_view()),
    path("contact-detail/<pk>", ContactDetailView.as_view()),
]