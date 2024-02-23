from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "country_code",
            "phone_number",
            "contact_picture",
            "is_favourite",
            "group",
            "created_at",
            "updated_at",
        ]

        read_only_fileds = ["created_at", "updated_at"]

