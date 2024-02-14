#django imports
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings
#DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
#local imports
from .serialiers import UserSerializer
from .auth import JWTAuthentication
from .models import User

import jwt


tags = ['Auth']

class RegisterView(APIView):
    serializer_class = UserSerializer

    @extend_schema(
        tags=tags,
        summary="Register a new user",
        description="This endpoint registers a new user",
        request=UserSerializer,
        responses={"201": UserSerializer}
    )
    def post(self,request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            User.objects.create_user(**data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginVIew(APIView):
    serializer_class = UserSerializer

    @extend_schema(
            tags=tags,
            summary="Login a user",
            description="This endpoint logs a user in",
            request=UserSerializer,
            responses={"200": UserSerializer}
    )
    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get('password')

        #authenticate the user
        user = authenticate(email=email, password=password)
        if user:
            payload = {"email":user.email, "first_name":user.first_name}
            token = jwt.encode(
                payload, settings.JWT_SECRET)
            serializer = self.serializer_class(user)
        
            return Response({"user":serializer.data, "token":token})
        else:
            return Response({"error": "Authentication failed"})
        