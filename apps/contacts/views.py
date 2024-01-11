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
    
