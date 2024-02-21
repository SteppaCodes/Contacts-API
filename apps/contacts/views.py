from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.pagination import PageNumberPagination

from .models import Contact, Favourite
from .serializers import ContactSerializer, FavouritesSerializer

tags = [["Contacts"], ["Favourites"]]

# V2
# TODO search contacts


class ContactListCreateAPIView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    page_size = 10

    @extend_schema(
        tags=tags[0],
        summary="Retrieve contacts",
        description="This endpoint retrieves contacts belonging to the authenticated user.",
        responses={200: ContactSerializer},
        parameters=[OpenApiParameter(
            name="query", 
            description="contact first or last name ", 
            required=False, type=str
            )
        ]
    )
    def get(self, request):
        query= request.GET.get("query")
        if query == None:
            query = ''
        contacts = Contact.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query),owner=request.user).order_by("first_name", "last_name")

        paginated_objects = self.paginate_queryset(contacts, request, view=self)
        serializer = self.serializer_class(paginated_objects, many=True)
        return self.get_paginated_response({"data": serializer.data})

    @extend_schema(
        tags=tags[0],
        summary="Create a new contact",
        description="This endpoint creates a new contact for the authenticated user.",
        request=ContactSerializer,
        responses={201: ContactSerializer},
        examples=[
            OpenApiExample(
                name="Create Contact Example",
                value={
                    "first_name": "John",
                    "last_name": "Doe",
                    "country_code": "234",
                    "contact_picture": "https://www.shutterstock.com/image-vector/microblog-platform-abstract-concept-vector-illustration-1852998859",
                    "phone_number": "1234567890",
                },
                description="Example request body for creating a contact.",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        # remove the created_at and updated_at fields from the response
        data = serializer.data
        data.pop("created_at")
        data.pop("updated_at")
        return Response({"data": data}, status=201)


class ContactDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    @extend_schema(
        tags=tags[0],
        summary="Retrieve a contact's detail",
        description="This endpoint retreives a contact's detail",
        responses={200: ContactSerializer},
    )
    def get(self, request, pk):

        try:
            contact = Contact.objects.get(pk=pk)
            serializer = self.serializer_class(contact)
            return Response(serializer.data)
        except:
            return Response({"error": "Contact not found"}, status=404)

    @extend_schema(
        tags=tags[0],
        summary="Update a contact's detail",
        description="This endpoint updates a contact's detail",
        responses={200: ContactSerializer},
    )
    def put(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = self.serializer_class(contact, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @extend_schema(
        tags=tags[0],
        summary="Delete a contact",
        description="This endpoint deletes a contact belonging to the authenticated user.",
        responses={204: ContactSerializer},
    )
    def delete(self, request, id):
        contact = Contact.objects.filter(id=id).first()
        if contact:
            contact.delete()
            return Response({"Successsful": "Deleted successfully"})
        else:
            return Response({"error": "Contact not found"}, status=404)


class FavouritesListCreateAPIView(APIView):
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags[1],
        summary="Retrieve favourites",
        description="This endpoint retreives the authenticated user's favourite contacts.",
        responses={200: FavouritesSerializer},
        parameters=[OpenApiParameter(
            name="query", 
            description="contact first or last name ", 
            required=False, type=str
            )
        ]
    )
    def get(self, request):
        query= request.GET.get("query")
        if query == None:
            query = ''

        favourites = Favourite.objects.filter(
            Q(contact__first_name__icontains=query) |
            Q(contact__last_name__icontains=query), 
            owner=request.user
            )
        serializer = self.serializer_class(favourites, many=True)
        return Response({"data": serializer.data})

    @extend_schema(
        tags=tags[1],
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
        tags=tags[1],
        summary="Remove favourite",
        description="This endpoint removes a contact from user's favourites list",
        responses={204: ContactSerializer},
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



