from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from authentication.exception import CustomError
from bitpin.models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress
from exchange.error_codes import ERRORS
from .permissions import BitPinCurrencyPermission, WalletAddressPermission, BitPinNetworkPermission
from .serializers import CurrencySerializer, NetworkSerializer, WalletAddressSerializer, \
    WalletAddressCreateSerializer, CurrencyUpdateSerializer


class CurrencyView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = [BitPinCurrencyPermission]
    serializer_class = CurrencySerializer

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


class CurrencyDetailView(generics.RetrieveUpdateAPIView):
    lookup_field = "id"
    queryset = BitPinCurrency.objects.all()
    http_method_names = ["get", "patch"]
    permission_classes = [BitPinCurrencyPermission
                          ]

    @property
    def authentication_classes(self):
        return [] if self.request.method == "GET" else [TokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CurrencySerializer
        return CurrencyUpdateSerializer  # CurrencyUpdateSerializer

    @swagger_auto_schema(operation_id=_("Get Currency Detail"))
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Update Currency Markup Percent"))
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, context={"partial": True})
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        return Response({
            "result": "success",
            "object": CurrencySerializer(updated_instance).data
        })


class NetworkView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsModerator, BitPinNetworkPermission]
    serializer_class = NetworkSerializer

    def get_queryset(self):
        return BitPinNetwork.objects.all()

    @swagger_auto_schema(operation_id=_("Get Network List"))
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True).data
        return Response({
            "result": "success",
            "objects": serializer
        }, status=status.HTTP_200_OK)


class WalletAddressView(generics.ListAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    queryset = BitPinWalletAddress.objects.all()
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & WalletAddressPermission)]

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return WalletAddressSerializer
        return WalletAddressCreateSerializer

    def get_queryset(self):
        is_moderator = self.is_moderator(self.request)
        currency_code = self.request.GET.get("currency_code")
        network_code = self.request.GET.get("network_code")
        if not is_moderator and not currency_code and not network_code:
            raise CustomError(ERRORS.custom_message_error(_("currency_code and network_code are required.")))
        lookup = {}
        if currency_code:
            lookup.update({"currency_id__code__exact": currency_code})
        if network_code:
            lookup.update({"network_id__code__exact": network_code})
        q = self.queryset.filter(**lookup)
        if q.count() > 1 and not is_moderator:
            raise PermissionError()
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
    http_method_names = ["get", "patch", "delete"]
    queryset = BitPinWalletAddress.objects.all()
    serializer_class = WalletAddressSerializer
    permission_classes = [IsModerator, WalletAddressPermission]
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

    @swagger_auto_schema(operation_id=_("Delete Wallet Address"))
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({
            "result": "success"
        })
