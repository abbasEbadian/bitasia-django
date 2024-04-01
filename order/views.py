from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


class OrderView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = []
    serializer_class = []

    def paginator(self):
        return False

    def get_queryset(self):
        return Order.objects.all()

    @swagger_auto_schema(operation_id=_("Get Order List"))
    def get(self, request):
        serializer = OrderSerializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)
