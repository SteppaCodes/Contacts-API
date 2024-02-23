from rest_framework import serializers

from .models import Favourite
from apps.contacts.models import Contact


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = [
            "id",
            "contact",
        ]

    def validate(self, attrs):
        contact = attrs.get("contact")
        favourites = Favourite.objects.filter(contact=contact).first()

        contacts = Contact.objects.filter(id=contact.id).first()
        if not contacts:
            raise serializers.ValidationError({"error": "Contact does not exist"})
        else:
            attrs["contact"] = contacts
        if favourites:
            raise serializers.ValidationError({"error": "Contact already in favourites"})
        return attrs
    

