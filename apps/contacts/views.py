from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response  import Response

from . models import Contact
from apps.accounts.auth import JWTAuthentication
from .serializers import ContactSerializer


class ContactListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get(self, request):
        contacts = Contact.objects.filter(owner=request.user)
        serializer = self.serializer_class(contacts, many=True)
        return Response(serializer.data)
    
