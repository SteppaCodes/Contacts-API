from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
        ]

 
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(min_length=5, write_only=True)
    password2 = serializers.CharField(min_length=5, write_only=True)
    terms_agreement = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "terms_agreement"
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        terms_agreement = attrs.get("terms_agreement")

        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError({"error": "User with this Email already exists"}) 

        if password1!= password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        if not terms_agreement:
            raise serializers.ValidationError({"error": "You must agree to terms and conditions"})

        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password2")
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

