from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .schema import create_user_schema, list_user_schema
from .serializer import UserSerializer, UserUpdateSerializer, UserCreateSerializer

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
