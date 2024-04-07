from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.response import Response

from permission.permissions import IsSuperUser
from permission.serializers import PermissionSerializer, GroupSerializer, GroupCreateSerializer

EXCLUDED_MODELS = ["logentry", "contenttype", "authtoken", "session", "currency"]


class PermissionView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsSuperUser]
    serializer_class = PermissionSerializer

    def paginator(self):
        return False

    def get_queryset(self):
        return Permission.objects.filter(~Q(content_type__model__in=EXCLUDED_MODELS))

    @swagger_auto_schema(operation_id="Get Permission List", tags=["Permissions"])
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })


class GroupView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsSuperUser]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def paginator(self):
        return False

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return GroupSerializer
        return GroupCreateSerializer

    @swagger_auto_schema(operation_id="Get Group List", tags=["Permissions"])
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id="Create New Group", tags=["Permissions"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "success",
            "object": serializer.data
        })
