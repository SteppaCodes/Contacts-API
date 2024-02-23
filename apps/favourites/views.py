from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from .serializers import FavouritesSerializer
from .models import Favourite

tags = ["Favourites"]


class FavouritesListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]
    page_size = 5

    @extend_schema(
        tags=tags,
        summary="Retrieve favourites",
        description="This endpoint retreives the authenticated user's favourite contacts.",
        responses={200: FavouritesSerializer},
        parameters=[
            OpenApiParameter(
                name="query",
                description="contact first or last name ",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="page", description="Page number", required=False, type=int
            ),
        ],
    )
    def get(self, request):
        query = request.GET.get("query")
        if query == None:
            query = ""

        favourites = Favourite.objects.filter(
            Q(contact__first_name__icontains=query)
            | Q(contact__last_name__icontains=query),
            owner=request.user,
        )
        paginated_qs = self.paginate_queryset(favourites, request, view=self)
        serializer = self.serializer_class(paginated_qs, many=True)
        return self.get_paginated_response({"data": serializer.data})

    @extend_schema(
        tags=tags,
        summary="Create favourites",
        description="This endpoint adds a new contact to the authenticated user's favourite contacts.",
        request=FavouritesSerializer,
        responses={201: FavouritesSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.validated_data["contact"]
        contact.is_favourite = True
        contact.save()
        serializer.save(owner=request.user)
        return Response({"data": serializer.data}, status=201)


class FavouriteDetailAPIView(APIView):
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Remove favourite",
        description="This endpoint removes a contact from user's favourites list",
        responses={204: FavouritesSerializer},
    )
    def delete(self, request, id):
        favourite = Favourite.objects.filter(id=id).first()

        if favourite:
            contact = favourite.contact

            contact.is_favourite = False
            contact.save()
            favourite.delete()
            return Response({"Successsful": "Deleted successfully"})
        else:
            return Response({"error": "Contact not found"})


