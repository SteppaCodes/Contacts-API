#django imports
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings
#DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
#local imports
from .serialiers import UserSerializer
from .auth import JWTAuthentication
from .models import User

import jwt

class RegisterView(APIView):
    serializer_class = UserSerializer
    def post(self,request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            User.objects.create_user(**data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginVIew(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get('password')

        #authenticate the user
        user = authenticate(email=email, password=password)
        if user:
            token = jwt.encode(
                {"email":user.email}, settings.JWT_SECRET
            )
            serializer = UserSerializer(user)
        
            return Response({"user":serializer.data, "token":token})
        else:
            return Response({"error": "Authentication failed"})
        