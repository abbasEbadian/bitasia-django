from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from notification.models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ["seen_user_ids", "user_id", "write_date"]

    def to_representation(self, instance):
        user = self.context.get("user", None)

        user = user or getattr(self.context.get("request"), "user", None)
        ret = super().to_representation(instance)
        if user:
            ret["seen"] = instance.seen_user_ids.filter(id=user.id).exists()
        return ret


class NotificationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ["seen_user_ids"]


class NotificationCreateSerializer(serializers.Serializer):
    user_ids = serializers.CharField(required=False, help_text="Comma separated list of user ids (no space)",
                                     allow_blank=True, allow_null=True)
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)

    def validate(self, attrs):
        user_ids = attrs.get("user_ids", "")
        users = User.objects.none()
        if user_ids:
            try:
                users = User.objects.filter(id__in=[int(x) for x in user_ids.split(",")])
            except User.DoesNotExist as e:
                raise CustomError(ERRORS.custom_message_error(_("Provided user_ids is not valid")))
        attrs["users"] = users
        attrs["type"] = Notification.NotificationType.GLOBAL if not users else Notification.NotificationType.USER
        return attrs


class NotificationSeenUpdateSerializer(serializers.Serializer):
    notifications_ids = serializers.CharField(required=True,
                                              help_text="Comma separated list of notification ids (no space)")

    def validate(self, attrs):
        try:
            notifications_ids = [int(x) for x in attrs.get("notifications_ids", "").split(",")]
        except ValueError as e:
            raise CustomError(ERRORS.custom_message_error(_("Provided notifications_ids is not valid")))
        notifications = Notification.objects.filter(id__in=notifications_ids)
        if len(notifications_ids) != len(notifications):
            raise CustomError(ERRORS.custom_message_error(_("Provided notifications_ids are not valid")))
        attrs["notifications"] = notifications
        return attrs
