# django imports
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

# local imports
from .serializers import (LoginSerialzer, RegisterSerializer)
from .models import User

import jwt


tags = ["Auth"]


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        tags=tags,
        summary="Register a new user",
        description="This endpoint registers a new user",
        request=RegisterSerializer,
        responses={"201": RegisterSerializer},
    )
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class LoginVIew(APIView):
    serializer_class = LoginSerialzer

    @extend_schema(
        tags=tags,
        summary="Login a user",
        description="This endpoint logs a user in",
        request=LoginSerialzer,
        responses={"200": LoginSerialzer},
        examples=[
            OpenApiExample(
                name="Login User example",
                value={
                    "email": "steppaapitestuser@gmail.com",
                    "password": "testuser",
                },
                description="Example request for authenticating a user",
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)
