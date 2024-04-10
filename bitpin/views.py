from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.mixins import IsAdminRequestMixin
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
        activity_filters = {"bitasia_active": True, "price_info_price__gt": 0}
        filters = {}
        if show_inactive and show_inactive != 'false':
            activity_filters = {}
        if for_dashboard and for_dashboard != 'false':
            filters.update({"show_in_dashboard": True})
        filters.update(activity_filters)
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


class CurrencyDetailView(generics.RetrieveUpdateAPIView, IsAdminRequestMixin):
    lookup_field = "id"
    queryset = BitPinCurrency.objects.all()
    http_method_names = ["get", "patch"]

    @property
    def authentication_classes(self):
        if self.request.method == "GET":
            return []
        return [TokenAuthentication]

    @property
    def permission_classes(self):
        if self.request.method == "GET":
            return []
        if self.has_admin_header(self.request.META):
            return [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CurrencySerializer
        # TODO Implement CurrencyUpdateSerializer
        return CurrencySerializer  # CurrencyUpdateSerializer

    @swagger_auto_schema(operation_id=_("Get Currency Detail"))
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Update Currency Markup Percent"))
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        return Response({
            "result": "success",
            "object": CurrencySerializer(updated_instance).data
        })


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


class WalletAddressView(generics.ListAPIView, IsAdminRequestMixin):
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
            lookup.update({"currency_id__code__exact": currency_code})
        if network_code:
            lookup.update({"network_id__code__exact": network_code})
        q = self.queryset.filter(**lookup)
        print(currency_code, network_code)
        print(len(q), self.has_admin_header(self.request.META))
        if len(q) > 1 and not self.has_admin_header(self.request.META):
            return self.queryset.none()
        return q

    @swagger_auto_schema(operation_id=_("Get Wallet Address List"), manual_parameters=[
        openapi.Parameter(name="currency_code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter(name="network_code", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ])
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Create new Wallet Address"))
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
