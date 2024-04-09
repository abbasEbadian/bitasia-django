from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from bitpin.models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress
from .serializers import CurrencySerializer, NetworkSerializer, CurrencyDashboardSerializer, WalletAddressSerializer, \
    WalletAddressCreateSerializer


class CurrencyView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = CurrencySerializer

    def get_serializer_class(self):
        for_dashboard = self.request.GET.get("for_dashboard", False)
        if for_dashboard:
            return CurrencyDashboardSerializer
        return CurrencySerializer

    def get_queryset(self):
        request = self.request
        show_inactive = request.GET.get("show_inactive", False)
        for_dashboard = request.GET.get("for_dashboard", False)
        filters = {}
        if show_inactive and show_inactive != 'false':
            filters.update({"bitasia_active": True})
        if for_dashboard and for_dashboard != 'false':
            filters.update({"show_in_dashboard": True})
        return BitPinCurrency.objects.filter(**filters)

    @swagger_auto_schema(operation_id=_("Get Currency List"), manual_parameters=[
        openapi.Parameter(name="show_inactive", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        openapi.Parameter(name="for_dashboard", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
    ])
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)


class CurrencyDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CurrencySerializer
    lookup_field = "id"
    queryset = BitPinCurrency.objects.all()

    @swagger_auto_schema(operation_id=_("Get Currency Detail"))
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)


class NetworkView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = NetworkSerializer

    def paginator(self):
        return False

    def get_queryset(self):
        return BitPinNetwork.objects.all()

    @swagger_auto_schema(operation_id=_("Get Network List"))
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)


class WalletAddressView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = BitPinWalletAddress.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return WalletAddressSerializer
        return WalletAddressCreateSerializer

    @property
    def permission_classes(self):
        if self.request.method.lower() == "get":
            return [IsAuthenticated]
        return [IsAdminUser]

    def get_queryset(self):
        currency_code = self.request.GET.get("currency_code")
        network_code = self.request.GET.get("network_code")
        lookup = {}
        if currency_code:
            lookup.update({"currency_id__code": currency_code})
        if network_code:
            lookup.update({"network_id__code": network_code})

        return self.queryset.filter(**lookup)

    @swagger_auto_schema(operation_id=_("Get Wallet Address List"), manual_parameters=[
        openapi.Parameter(name="currency_code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="network_code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newb = serializer.save()
        return Response({
            "result": "success",
            "object": WalletAddressSerializer(newb).data
        }, status=status.HTTP_201_CREATED)


class WalletAddressDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ["get", "patch"]
    queryset = BitPinWalletAddress.objects.all()
    serializer_class = WalletAddressSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"

    @swagger_auto_schema(operation_id=_("Get Wallet Address Detail"))
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_object()).data
        })

    @swagger_auto_schema(operation_id=_("Update Wallet Address"))
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "success",
            "object": serializer.data
        })
