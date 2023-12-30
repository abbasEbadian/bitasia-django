from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from exchange import error_codes as ERRORS
from .exception import CustomError
from .utils import check_mobile

User = get_user_model()


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


"""
'null': 'This field cannot be null.'
'blank': 'This field cannot be blank.'
'invalid' : 'Enter a valid email address.'
'invalid_choice': 'Value is not a valid choice.'
'required': 'This field is required.'
'max_length': '...'
'min_length': '...'
'max_value': '...'
'min_value': '...'
'max_digits': '...'
'invalid_list': '...'
'max_decimal_places': '....'
'empty': '....'
"""
