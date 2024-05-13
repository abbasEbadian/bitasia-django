from django.contrib.auth import authenticate, get_user_model
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authority.models import AuthorityRule
from exchange.error_codes import ERRORS
from users.models import LoginHistory
from .exception import CustomError
from .utils import check_mobile

User = get_user_model()
BIRTHDAY_FORMAT = r"^\d{4}-\d{2}-\d{2}$"


# Generate otp for login
# Check mobile and password
class OtpSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, attrs):

        mobile = attrs.get('mobile')
        password = attrs.get('password', "")

        if not mobile or not check_mobile(mobile) or len(mobile) != 11:
            raise CustomError(ERRORS.ERROR_INVALID_MOBILE)
        if not password:
            raise CustomError(ERRORS.ERROR_INVALID_PASSWORD)
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            raise CustomError(ERRORS.ERROR_USER_DOES_NOT_EXIST)
        if not user.check_password(password):
            user.log_login(successful=False, ip=self.context.get("request").META.get('REMOTE_ADDR', "0.0.0.0"),
                           reason=LoginHistory.Reason.INVALID_PASSWORD)
            raise CustomError(ERRORS.ERROR_WRONG_PASSWORD)
        attrs['user'] = user
        return attrs


class VerifyOtpSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False)
    otp = serializers.CharField(required=False)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        otp = attrs.get('otp')
        if not mobile:
            raise CustomError(ERRORS.ERROR_INVALID_MOBILE)
        if not otp:
            raise CustomError(ERRORS.ERROR_INVALID_OTP)
        if not User.objects.filter(mobile=mobile).exists():
            raise CustomError(ERRORS.ERROR_USER_DOES_NOT_EXIST)
        _user = User.objects.filter(mobile=mobile).first()
        user = authenticate(request=self.context.get('request'), otp=otp, mobile=mobile)
        if not user:
            _user.log_login(successful=False, ip=self.context.get("request").META.get('REMOTE_ADDR', "0.0.0.0"),
                            reason=LoginHistory.Reason.INVALID_OTP)
            raise CustomError(ERRORS.ERROR_WRONG_OTP)
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    referral = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        referral = attrs.get('referral')

        if not mobile or not check_mobile(mobile) or len(mobile) != 11:
            raise CustomError(ERRORS.ERROR_INVALID_MOBILE)
        if not password or len(password) < 6:
            raise CustomError(ERRORS.ERROR_INVALID_PASSWORD_PATTERN)
        if not first_name or len(first_name) < 3:
            raise CustomError(ERRORS.ERROR_INVALID_FIRST_NAME)
        if not last_name or len(last_name) < 3:
            raise CustomError(ERRORS.ERROR_INVALID_LAST_NAME)
        if referral and not User.objects.only("referral_code").filter(referral_code=referral).exists():
            raise CustomError(ERRORS.custom_message_error(_("Invalid referral code")))
        parent = User.objects.filter(referral_code=referral)
        if User.objects.filter(mobile=mobile).exists():
            raise CustomError(ERRORS.ERROR_MOBILE_ALREADY_EXISTS)
        vals = dict(mobile=mobile, username=mobile, first_name=first_name,
                    last_name=last_name)
        if parent:
            vals["parent"] = parent

        user = User.objects.create_user(**vals)
        user.set_password(password)
        user.save()
        attrs['user'] = user

        return attrs


class VerifyAccountSerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(required=True)
    first_name = serializers.CharField(min_length=3, required=False)
    last_name = serializers.CharField(min_length=3, required=False)
    national_code = serializers.CharField(min_length=10, max_length=10, required=False)
    birthdate = serializers.RegexField(BIRTHDAY_FORMAT, required=False)
    gender = serializers.ChoiceField(choices=(('male', _('Male')), ('female', _('Female'))), required=False)
    national_card_image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
        required=False)
    birth_card_image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
        required=False)

    def validate(self, attrs, **kw):
        rule_id = attrs.get('rule_id', None)
        rule = get_object_or_404(AuthorityRule, pk=int(rule_id))
        if not rule: raise CustomError(ERRORS.ERROR_INVALID_RULE)
        fields = list(map(lambda x: x.field_key, rule.option_ids.all()))
        for field in fields:
            value = attrs.get(field, None)
            if not value:
                raise CustomError(ERRORS.GENERAL_UNMET_PARAMS_ERROR)
        del attrs['rule_id']
        return attrs
