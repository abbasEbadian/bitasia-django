from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from permission.serializers import LoginHistorySerializer
from .models import LoginHistory
from .permission import LoginHistoryPermissions
from .schema import create_user_schema, list_user_schema
from .serializer import UserSerializer, UserUpdateSerializer, UserCreateSerializer

User = get_user_model()


# Create your views here.
class UserListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsModerator,)

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(**list_user_schema)
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserCurrentUserView(generics.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    @swagger_auto_schema(operation_id="Current user detail")
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(request.user).data
        })


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


class UserDetailView(generics.RetrieveUpdateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsModerator]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_object()).data
        })

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            "result": "success",
            "object": UserSerializer(instance, context={"is_moderator": self.is_moderator(self.request)}).data
        })


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
