from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from bitpin.models import BitPinCurrency, BitPinNetwork


class CurrencyView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = []

    def paginator(self):
        return False

    def get_queryset(self):
        return BitPinCurrency.objects.all()

    @swagger_auto_schema(operation_id=_("Get Currency List"))
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)


class NetworkView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = []
    serializer_class = []

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
