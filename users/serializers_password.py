from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from authentication.models import OTP
from exchange.error_codes import ERRORS

User = get_user_model()


class VerifyForgetPasswordSerializer(serializers.Serializer):
    password_1 = serializers.CharField(required=True, min_length=6)
    password_2 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, min_length=5, max_length=5)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate(self, attrs):
        password_1 = attrs.get('password_1')
        password_2 = attrs.get('password_2')
        mobile = attrs.get('mobile')
        _otp = attrs.get('otp')
        user = User.objects.filter(mobile=mobile)
        if not user.exists():
            raise CustomError(ERRORS.custom_message_error(_("User not found.")))
        if password_1 != password_2:
            raise CustomError(ERRORS.custom_message_error(_("Passwords doesn't match.")))
        user = user.first()
        otp = OTP.objects.filter(user_id=user, code=_otp, type=OTP.Type.FORGET_PASSWORD)
        if not otp.exists():
            raise CustomError(ERRORS.custom_message_error(_("Wrong OTP.")))
        attrs["otp_id"] = otp.first()
        attrs["user"] = user

        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        password = validated_data.get("password_1")
        otp = validated_data["otp_id"]
        otp.consume()
        user.set_password(password)
        user.save(update_fields=["password"])
        return otp


class ForgetPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        user = User.objects.filter(mobile=mobile)
        if not user.exists():
            raise CustomError(ERRORS.custom_message_error(_("User not found.")))
        attrs["user"] = user.first()
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        otp = user.send_otp(otp_type=OTP.Type.FORGET_PASSWORD)
        return otp


class VerifyResetPasswordSerializer(serializers.Serializer):
    password_1 = serializers.CharField(required=True, min_length=6)
    password_2 = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate(self, attrs):
        password_1 = attrs.get('password_1')
        password_2 = attrs.get('password_2')
        old_password = attrs.get('old_password')
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise CustomError(ERRORS.custom_message_error(_("Wrong password")))
        if password_1 != password_2:
            raise CustomError(ERRORS.custom_message_error(_("Passwords doesn't match.")))
        attrs["user"] = user

        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        password = validated_data.get("password_1")
        user.set_password(password)
        user.save(update_fields=["password"])
        return user
