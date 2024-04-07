from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type_id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = ContentType.objects.get(id=data["content_type_id"]).model
        del data["content_type_id"]
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]
        depth = 1


class GroupCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    permission_ids = serializers.CharField(max_length=255)

    def validate(self, attrs):
        permission_ids = [str(x).strip() for x in attrs.get("permission_ids", "").split(",")]
        name = attrs.get("name")
        if not permission_ids:
            return CustomError(ERRORS.custom_message_error(_("Permission IDs must not be empty.")))

        if Group.objects.filter(name=name):
            return CustomError(ERRORS.custom_message_error(_("Group with this name already exists.")))

        permission_ids = Permission.objects.filter(id__in=permission_ids)
        group = Group.objects.create(name=name)
        group.permissions.set(permission_ids)
        return attrs
