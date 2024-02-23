from django.urls import path 

from .views import GroupListCreateAPIView, GroupDetailAPIView


urlpatterns = [
    path("groups/", GroupListCreateAPIView.as_view()),
    path("groups/<id>", GroupDetailAPIView.as_view())
]