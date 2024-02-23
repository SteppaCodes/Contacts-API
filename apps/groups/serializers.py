from rest_framework import serializers

from .models import Group
from apps.contacts.serializers import ContactSerializer


class GroupSerializer(serializers.ModelSerializer):
    num_of_contacts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "num_of_contacts",
        ]

    def get_num_of_contacts(self, obj):
        return obj.group_contacts.count()


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "description"]

        read_only_fields = ["id"]

    def validate(self, attrs):
        name = attrs.get("name")
        group = Group.objects.filter(name=name).first()
        if group:
            raise serializers.ValidationError({"error": "Group already exists"})
        else:
            return attrs


# class GroupDetailSerializer(GroupSerializer):
#     group_contacts = ContactSerializer(read_only=True)

#     class Meta(GroupSerializer.Meta):
#         fields = GroupSerializer.Meta.fields + ["group_contacts"]
