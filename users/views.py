from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializer import UserSerializer, UserUpdateSerializer

User = get_user_model()


# Create your views here.
class UserListView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    serializer_class = UserSerializer
    queryset = User.objects.all()




