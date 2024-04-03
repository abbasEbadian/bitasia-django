from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from bitpin.models import BitPinCurrency, BitPinNetwork
from .serializers import CurrencySerializer, NetworkSerializer


class CurrencyView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = CurrencySerializer

    def paginator(self):
        return False

    def get_queryset(self):
        request = self.request
        show_inactive = request.GET.get("show_inactive", False)
        filters = {"bitasia_active": True}
        if show_inactive and show_inactive != 'false':
            filters = {}
        return BitPinCurrency.objects.filter(**filters)

    @swagger_auto_schema(operation_id=_("Get Currency List"), manual_parameters=[
        openapi.Parameter(name="show_inactive", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
    ])
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
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
