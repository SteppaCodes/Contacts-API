from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from . models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name =serializers.CharField(max_length=200)
    last_name =serializers.CharField(max_length=200)
    password =serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            "password",
        ]

        def validate(self, attrs):
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "User with this Email already exists"})
            return super().validate(attrs)
        
        def create(self, validated_data):
            return User.objects.create_user(**validated_data)