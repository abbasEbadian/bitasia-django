from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from permission.serializers import LoginHistorySerializer
from .models import LoginHistory
from .permission import LoginHistoryPermissions
from .schema import create_user_schema, list_user_schema
from .serializer import UserSerializer, UserUpdateSerializer, UserCreateSerializer, VerifyForgetPasswordSerializer

User = get_user_model()


# Create your views here.
class UserListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(**list_user_schema)
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserCreateView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserCreateSerializer

    @swagger_auto_schema(**create_user_schema)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return User.objects.all()


class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDetailAdminView(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(operation_id="Get single user info",
                         security=[{"Token": []}])
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserDetailView(generics.RetrieveAPIView):
    allowed_methods = ["GET"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_id="get user info",
                         security=[{"Token": []}], repsonses={"200": openapi.Response("Success", examples={})})
    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer_class()
        return Response(serializer(user).data)

    def get_queryset(self, *args, **kwargs):
        return self.request.user

    def paginator(self):
        return None


class UserDeleteView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginHistoryView(generics.ListAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & LoginHistoryPermissions)]
    serializer_class = LoginHistorySerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return LoginHistory.objects.all()
        return LoginHistory.objects.filter(user_id=self.request.user)


@swagger_auto_schema(operation_id=_("Forget password"), tags=["User - Forget password"], method="POST",
                     request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                 required=["password_1", "password_2", "otp"],
                                                 properties={
                                                     "password_1": openapi.Schema(type=openapi.TYPE_STRING),
                                                     "password_2": openapi.Schema(type=openapi.TYPE_STRING),
                                                     "mobile": openapi.Schema(type=openapi.TYPE_STRING),
                                                     "otp": openapi.Schema(type=openapi.TYPE_STRING),
                                                 }))
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def forget_password_change_view(request):
    serializer = VerifyForgetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        "result": "success",
        "message": _('Password changed successfully')
    })
