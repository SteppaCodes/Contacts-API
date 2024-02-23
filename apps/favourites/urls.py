from django.urls import path

from .views import FavouritesListCreateAPIView, FavouriteDetailAPIView

urlpatterns = [
    path("favourites/", FavouritesListCreateAPIView.as_view()),
    path("favourites/<id>", FavouriteDetailAPIView.as_view())
]


