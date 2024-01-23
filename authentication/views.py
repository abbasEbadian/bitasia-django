from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, generics
from rest_framework import status
from rest_framework.response import Response

from authority.models import AuthorityRequest
from exchange import error_codes as ERRORS
from . import schema as atuh_schema
from .exception import CustomError
from .serializer import RegisterSerializer, OtpSerializer, VerifyOtpSerializer

User = get_user_model()
MOBILE_AUTHORITY = 1


class LoginView(KnoxLoginView):
    allowed_methods = ['POST']
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifyOtpSerializer

    @swagger_auto_schema(**atuh_schema.verify_otp_schema)
    def post(self, request, format=None):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        req, created = AuthorityRequest.objects.get_or_create(rule_id=MOBILE_AUTHORITY, user_id=user,
                                                              defaults={"approved": True})
        req.approve()
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class CreateOTPView(generics.CreateAPIView):
    allowed_methods = ['POST']
    permission_classes = [permissions.AllowAny]
    serializer_class = OtpSerializer

    @swagger_auto_schema(**atuh_schema.create_otp_schema_dict)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        sent = user.send_otp()
        if not sent:
            raise CustomError(ERRORS.ERROR_FAIL_TO_SEND_SMS)
        return Response({
            "result": "success",
            "message": _("Otp has been sent to your mobile.")
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    allowed_methods = ['POST']
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(**atuh_schema.register_schema)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.validated_data['user']
            if not user:
                raise Exception("Err")
            return Response(
                {"result": "success", "message": _('Account has been created')},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            raise CustomError(ERRORS.ERROR_INVALID_MOBILE)
