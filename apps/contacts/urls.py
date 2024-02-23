#dango imports
from django.urls import path
#Local imports
from . views import (ContactListCreateAPIView, ContactDetailAPIView)


urlpatterns = [
    path("contact-list/", ContactListCreateAPIView.as_view()),
    path("contact-detail/<id>", ContactDetailAPIView.as_view()),
]