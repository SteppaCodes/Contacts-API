from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
        ]

        def validate(self, attrs):
            email = attrs.get("email")
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "User with this Email already exists"}
                )
            return super().validate(attrs)

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)




class LoginSerialzer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'full_name',
            'access_token',
            'refresh_token'
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(_("email or password incorrect"))

        tokens = user.tokens()

        return {
            "email": user.email,
            "full_name": user.full_name,
            "access_token": str(tokens.get("access_token")),
            "refresh_token": str(tokens.get("refresh_token")),
        }
