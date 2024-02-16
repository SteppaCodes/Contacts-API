from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Contact
from .serializers import ContactSerializer

tags = ["Contacts"]

# V2
# TODO favourites list
# TODO search contacts


class ContactListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    @extend_schema(
        tags=tags,
        summary="Retrieve contacts",
        description="This endpoint retrieves contacts belonging to the authenticated user.",
        responses={200: ContactSerializer},
        # parameters=[OpenApiParameter(name="search", description="Search term", required=False, type=str)]
    )
    def get(self, request):
        contacts = Contact.objects.filter(owner=request.user)
        serializer = self.serializer_class(contacts, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=tags,
        summary="Create a new contact",
        description="This endpoint creates a new contact for the authenticated user.",
        request=ContactSerializer,
        responses={201: ContactSerializer},
        examples=[
            OpenApiExample(
                name="Create Contact Example",
                value={
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "1234567890",
                },
                description="Example request body for creating a contact.",
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)


class ContactDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    @extend_schema(
        tags=tags,
        summary="Retrieve a  contact's detail",
        description="This endpoint a contact's detail belonging to the authenticated user.",
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
        tags=tags,
        summary="Update a  contact's detail",
        description="This endpoint updates a contact's detail belonging to the authenticated user.",
        responses={200: ContactSerializer},
    )
    def put(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = self.serializer_class(contact, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


    @extend_schema(
        tags=tags,
        summary="Delete a contact",
        description="This endpoint deletes a contact belonging to the authenticated user.",
        responses={204: ContactSerializer},
    )
    def delete(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return Response({"Successsful": "Deleted successfully"})
