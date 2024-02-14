#dango imports
from django.urls import path
#Local imports
from . views import ContactListCreateAPIView, ContactDetailView


urlpatterns = [

    path("contact-list/", ContactListCreateAPIView.as_view()),
    path("contact-detail/<pk>", ContactDetailView.as_view()),
]