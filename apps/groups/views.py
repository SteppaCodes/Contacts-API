from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from .serializers import (
    GroupSerializer,
    CreateGroupSerializer,
)
from .models import Group
from apps.accounts.models import User
from apps.contacts.serializers import ContactSerializer


tags = ["Groups"]


class GroupListCreateAPIView(APIView, PageNumberPagination):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    page_size = 10

    @extend_schema(
        tags=tags,
        summary="Retrieve groups",
        description="This endpoint retrieves groups belonging to the authenticated user.",
        responses={200: GroupSerializer},
        parameters=[
            OpenApiParameter(
                name="page",
                description="Retrieve a particular page of groups. Defaults to 1",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="query",
                description="group name",
                required=False,
                type=str,
            ),
        ],
    )
    def get(self, request):
        query = request.GET.get("query")
        if query == None:
            query = ''

        user = User.objects.get(id=request.user.id)
        groups = user.user_groups.filter(Q(name__icontains=query))
        paginated_qs = self.paginate_queryset(groups, request, view=self)
        serializer = self.serializer_class(paginated_qs, many=True)
        return self.get_paginated_response({"data": serializer.data})

    @extend_schema(
        tags=tags,
        summary="Create a new group",
        description="This endpoint creates a new group",
        request=CreateGroupSerializer,
        responses={201: CreateGroupSerializer},
        examples=[
            OpenApiExample(
                name="Create group Example",
                value={
                    "name": "Sacred Circle",
                    "description": "Men I trust",
                },
                description="Example request body for creating a group.",
            )
        ],
    )
    def post(self, request):
        user = request.user
        serializer = CreateGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"data": serializer.data}, status=201)


class GroupDetailAPIView(APIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Retrieve a group's detail",
        description="This endpoint retreives a group's detail",
        responses={200: GroupSerializer},
    )
    def get(self, request, id):
        group = Group.objects.prefetch_related("group_contacts").get(id=id)
        contacts = group.group_contacts.all()

        contact_serialzizer = ContactSerializer(contacts, many=True)
        serializer = self.serializer_class(group)

        return Response({"data": serializer.data, "contacts": contact_serialzizer.data})

    @extend_schema(
        tags=tags,
        summary="Update a group's detail",
        description="This endpoint updates a contact's detail",
        responses={200: ContactSerializer},
    )
    def put(self, request, id):
        group = Group.objects.get(id=id)
        serializer = self.serializer_class(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Group Updated successfully"})

    @extend_schema(
        tags=tags,
        summary="Delete a group",
        description="This endpoint deletes a group",
        responses={200: ContactSerializer},
    )
    def delete(self, request, id):
        try:
            group = Group.objects.get(id=id)
            group.delete()
            return Response(_("Group deleted successfully"))
        except Group.DoesNotExist:
            return Response(_("Group not found"))
