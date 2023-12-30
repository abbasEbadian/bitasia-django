from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from .models import OTP

User = get_user_model()


class OtpAuthBackend(BaseBackend):
    def authenticate(self, request, otp=None, mobile=None):
        if not mobile or not otp:
            return None
        try:
            return OTP.objects.get(code=otp, user_id__mobile=mobile).user_id
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None