from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from users.models import LoginHistory
from users.serializer import UserSimplifiedSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "content_type_id"]
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cid = data.pop("content_type_id")
        data["category"] = ContentType.objects.get(pk=cid).model
        return data


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField("get_permissions")

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]
        depth = 1

    def get_permissions(self, instance):
        return PermissionSerializer(instance.permissions.filter(codename__startswith="view"), many=True).data


class GroupUpdateCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    permission_codes = serializers.CharField(max_length=255)

    def validate(self, attrs):
        permission_codes = [str(x).strip() for x in attrs.get("permission_codes", "").split(",")]
        name = attrs.get("name")
        if not permission_codes:
            raise CustomError(ERRORS.custom_message_error(_("Permission IDs must not be empty.")))

        if Group.objects.filter(name=name).exists():
            raise CustomError(ERRORS.custom_message_error(_("Group with this name already exists.")))
        perms = Permission.objects.all()
        new_perms = perms.none()
        for code in permission_codes:
            new_perms |= perms.filter(Q(codename__endswith=code) & ~Q(codename__startswith="delete"))
        # complement_permission_ids = Permission.objects.filter(model)
        attrs["permission_ids"] = new_perms
        return attrs

    def create(self, validated_data):
        permission_ids = validated_data.get("permission_ids")
        name = validated_data.get("name")
        group = Group.objects.create(name=name)
        group.permissions.set(permission_ids)
        return group

    def update(self, instance, validated_data):
        permission_ids = validated_data.get("permission_ids")
        name = validated_data.get("name")
        instance.permissions.set(permission_ids)
        instance.name = name
        instance.save(update_fields=["name", "permission_ids"])
        return instance


class LoginHistorySerializer(serializers.ModelSerializer):
    user_id = UserSimplifiedSerializer()

    class Meta:
        model = LoginHistory
        fields = "__all__"
        depth = 1
