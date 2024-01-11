from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response  import Response

from . models import Contact
from apps.accounts.auth import JWTAuthentication
from .serializers import ContactSerializer


class ContactListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get(self, request):
        contacts = Contact.objects.filter(owner=request.user)
        serializer = self.serializer_class(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
    
class ContactDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get(self, request, pk):
        
        try:
            contact = Contact.objects.get(pk=pk)
            serializer = self.serializer_class(contact)
            return Response(serializer.data)
        except:
            return Response({"error": "Contact not found"}, status=404)
    
    def put(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = self.serializer_class(contact, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return Response({"Successsful": "Deleted successfully"})
