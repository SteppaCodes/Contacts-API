#dango imports
from django.urls import path
#Local imports
from . views import (ContactListCreateAPIView, ContactDetailAPIView, FavouritesListCreateAPIView, FavouriteDetailAPIView)


urlpatterns = [
    path("contact-list/", ContactListCreateAPIView.as_view()),
    path("contact-detail/<id>", ContactDetailAPIView.as_view()),

    path("favourites/", FavouritesListCreateAPIView.as_view()),
    path("favourites/<id>", FavouriteDetailAPIView.as_view())
]