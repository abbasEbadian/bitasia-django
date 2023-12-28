import random
from typing import List

from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, serializers, generics, status

from django.contrib.auth import login, user_logged_in
from rest_framework.response import Response

from .models import OTP
from .schema import create_otp_schema_dict
from .serializer import OtpSerializer, AuthOtpSerializer
from .utils import send_otp_sms, check_mobile, check_email
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(User)
        serializer = AuthOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # login(request, user)
        return super(LoginView, self).post(request, format=None)


class CreateOTPView(generics.CreateAPIView):
    allowed_methods = ['POST']
    permission_classes = [permissions.AllowAny]
    serializer_class = OtpSerializer

    @swagger_auto_schema(responses=create_otp_schema_dict)
    def post(self, request, *args, **kwargs):
        print("TEST")
        method = request.data.get('method')
        mobile = request.data.get('mobile')
        email = request.data.get('email')

        if method not in ['mobile', 'email']:
            raise serializers.ValidationError(_('Invalid method'))
        if method == 'mobile' and not mobile:
            raise serializers.ValidationError(_('Must provide mobile'))
        if method == 'email' and not email:
            raise serializers.ValidationError(_('Must provide email'))

        sent = False
        otp = False

        if method == 'mobile':
            if not check_mobile(mobile):
                raise serializers.ValidationError(_('Invalid mobile'))
            otp, sent = send_otp_sms(mobile)
        else:
            if not check_email(email):
                raise serializers.ValidationError(_('Invalid mobile'))
                # result = send_otp_email(email)
        result = {"result": "success"}
        if not sent:
            raise serializers.ValidationError(_("Cant connect to sms provider"))
        user = User.objects.filter(mobile='09143708563')[0]
        # if not user:
        #     raise serializers.ValidationError(_("User does not exist"))

        user.otp_set.create(code=otp)
        return Response(result, status=status.HTTP_200_OK)



