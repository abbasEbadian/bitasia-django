from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order, Purchase
from order.permissions import CanConfirmPurchase
from order.serializers import OrderSerializer, OrderCreateDepositSerializer, OrderForAdminSerializer, \
    PurchaseSerializer, PurchaseCreateSerializer, PurchaseSubmitSerializer


class OrderView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def paginator(self):
        return False

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.request.user.is_staff:
                return OrderForAdminSerializer
            return OrderSerializer
        return OrderCreateDepositSerializer

    @swagger_auto_schema(operation_id=_("Get Order List"))
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Book a new deposit order"))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user_id": request.user})
        serializer.is_valid(raise_exception=True)
        valid_attrs = serializer.validated_data
        return Response({
            "result": "success",
            "object": OrderSerializer(valid_attrs["order_id"]).data
        }, status=status.HTTP_201_CREATED)


class PurchaseView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = []

    def paginator(self):
        return False

    def get_queryset(self):
        return Purchase.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return PurchaseSerializer
        return PurchaseCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Purchase List"))
    def get(self, request):
        serializer = PurchaseSerializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Create new purchase"))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user_id": request.user})
        serializer.is_valid(raise_exception=True)
        valid_attrs = serializer.validated_data
        return Response({
            "result": "success",
            "object": PurchaseSerializer(valid_attrs["purchase_id"]).data
        }, status=status.HTTP_201_CREATED)


class PurchaseAdminConfirmView(generics.UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [CanConfirmPurchase]
    serializer_class = PurchaseSubmitSerializer
    http_method_names = ["patch"]

    @swagger_auto_schema(operation_id=_("Submit a purchase"))
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        purchase = serializer.validated_data["purchase_id"]
        result, message = purchase.confirm()
        return Response({
            "result": result,
            "message": message
        })
