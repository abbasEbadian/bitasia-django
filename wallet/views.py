from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from wallet.models import Wallet
from wallet.permissions import WalletPermission
from wallet.serializers import WalletSerializer, WalletCreateSerializer


class WalletView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & WalletPermission)]
    queryset = Wallet.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return WalletSerializer
        return WalletCreateSerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Wallet.objects.all()
        return Wallet.objects.filter(user_id=self.request.user)

    @swagger_auto_schema(operation_id=_("Get Wallet List"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Generate new wallet"))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = serializer.save(user_id=request.user)
        return Response({
            "result": "success",
            "object": WalletSerializer(wallet).data
        })


class WalletDetailView(generics.RetrieveAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & WalletPermission)]
    serializer_class = WalletSerializer
    lookup_field = "id"

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Wallet.objects.all()
        return Wallet.objects.filter(user_id=self.request.user)

    @swagger_auto_schema(operation_id=_("Get Wallet Detail"))
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)
