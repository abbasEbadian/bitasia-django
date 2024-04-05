from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from bitpin.models import BitPinCurrency, BitPinNetwork
from .serializers import CurrencySerializer, NetworkSerializer, CurrencyDashboardSerializer


class CurrencyView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = CurrencySerializer

    def paginator(self):
        return False

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
