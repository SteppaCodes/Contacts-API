# django imports
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample

# local imports
from .serializers import (
                        LoginSerialzer,
                        RegisterSerializer,
                        VerifyOtpSerializer,
                        LogoutSerializer,
)
from .models import User, OneTimePassword
from .senders import SendMail

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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            SendMail.send_otp(user["email"])

        return Response(
            {
                "message": f"Hi {user['first_name']}, an otp has been sent to your email address, please provide this code to verify your email",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


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
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)


class VerifyOTPAPIView(APIView):
    serializer_class = VerifyOtpSerializer

    @extend_schema(
        tags=tags,
        summary="verify account",
        description="This endpoint verifies a user email address",
        request=VerifyOtpSerializer,
        responses={"200": VerifyOtpSerializer},
        examples=[
            OpenApiExample(
                name="Verify User example",
                value={
                    "otp": "234672",
                },
                description="Example request for verifying a user's email address",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_otp = serializer.validated_data["otp"]
        try:
            otp_code_object = OneTimePassword.objects.get(code=user_otp)
            user = otp_code_object.user

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                return Response(
                    {"success": "Congrats! your email has been verified successfully"}
                )
            return Response({"eeror": "Email has already been verified"})
        except OneTimePassword.DoesNotExist:
            return Response({"error": "OTP is invalid or expired"})


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    @extend_schema(
        tags=tags,
        summary="Logout a user",
        description="This endpoint logs a user out",
        request=LogoutSerializer,
        responses={"200": "success"}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK) 
