import re

from django.contrib.auth import authenticate, get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from exchange import error_codes as ERRORS
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
        user = authenticate(request=self.context.get('request'), otp=otp, mobile=mobile)
        if not user:
            raise CustomError(ERRORS.ERROR_WRONG_OTP)

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(required=True, allow_blank=False, trim_whitespace=False, min_length=8)
    first_name = serializers.CharField(required=True, allow_blank=False, min_length=3)
    last_name = serializers.CharField(required=True, allow_blank=False, min_length=6)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if not mobile or not check_mobile(mobile) or len(mobile) != 11:
            raise CustomError(ERRORS.ERROR_INVALID_MOBILE)
        if not password:
            raise CustomError(ERRORS.ERROR_INVALID_PASSWORD)
        if not first_name or len(first_name) < 3:
            raise CustomError(ERRORS.ERROR_INVALID_FIRST_NAME)
        if not last_name or len(last_name) < 3:
            raise CustomError(ERRORS.ERROR_INVALID_LAST_NAME)

        if User.objects.filter(mobile=mobile).exists():
            raise CustomError(ERRORS.ERROR_MOBILE_ALREADY_EXISTS)

        user = User.objects.create_user(mobile=mobile, password=password, username=mobile, first_name=first_name,
                                        last_name=last_name)
        attrs['user'] = user

        return attrs


class VerifyAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=3)
    last_name = serializers.CharField(min_length=3)
    birthdate = serializers.RegexField(BIRTHDAY_FORMAT)
    gender = serializers.ChoiceField(choices=(('male', _('Male')), ('female', _('Female'))))
    image_name = serializers.ChoiceField(choices=(('national_card', 'National Card'), ('birth_card', 'Birth Card')))
    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])])

    def validate(self, attrs, **kw):
        first_name = attrs.get('first_name', None)
        if not first_name: raise ValidationError(ERRORS.ERROR_INVALID_FIRST_NAME)

        last_name = attrs.get('first_name', None)
        if not last_name: raise ValidationError(ERRORS.ERROR_INVALID_LAST_NAME)

        birthdate = attrs.get('birthdate', None)
        ok_bd = re.compile(BIRTHDAY_FORMAT).match(birthdate)
        if not birthdate or not ok_bd:
            raise ValidationError(ERRORS.ERROR_INVALID_BIRTHDATE)

        gender = attrs.get('gender', None)
        if not gender: raise ValidationError(ERRORS.ERROR_INVALID_GENDER)

        return attrs
