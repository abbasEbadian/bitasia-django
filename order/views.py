from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from authentication.exception import CustomError
from bitpin.models import BitPinCurrency, BitPinNetwork
from exchange.error_codes import ERRORS
from order.models import Transaction, Order, Transfer
from order.permissions import TransactionPermission, OrderPermission
from order.serializers import TransactionSerializer, TransactionForAdminSerializer, TransactionCreateSerializer, \
    TransactionUpdateSerializer, OrderForAdminSerializer, OrderCreateSerializer, OrderSerializer, TransferSerializer, \
    TransferCreateSerializer, CalculateOrderCommissionSerializer

CRYPTO_TRANSACTION_TAGS = ["Transactions - Crypto"]
ORDER_TAGS = ["Orders"]
TRANSFER_TAGS = ["Transfers"]


class TransactionView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & TransactionPermission)]
    pagination_class = LimitOffsetPagination
    default_limit = 50

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Transaction.objects.all()
        return Transaction.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.is_moderator(self.request):
                return TransactionForAdminSerializer
            return TransactionSerializer
        return TransactionCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Transaction List"), tags=CRYPTO_TRANSACTION_TAGS)
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Book a new Transaction"), tags=CRYPTO_TRANSACTION_TAGS)
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data, context={"user_id": self.request.user})
            serializer.is_valid(raise_exception=True)
            newb = serializer.save()
        return Response({
            "result": "success",
            "object": TransactionSerializer(newb).data
        }, status=status.HTTP_201_CREATED)


class TransactionDetailView(generics.RetrieveUpdateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    # permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & TransactionPermission)]
    queryset = Transaction.objects.all()
    lookup_field = "id"
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.is_moderator(self.request):
                return TransactionForAdminSerializer
            return TransactionSerializer
        return TransactionUpdateSerializer

    def get_queryset(self):
        if self.is_moderator(self.request):
            return self.queryset
        return self.queryset.filter(user_id=self.request.user)

    @swagger_auto_schema(operation_id="Get Transaction Detail", tags=CRYPTO_TRANSACTION_TAGS)
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })

    @swagger_auto_schema(operation_id="Accept/Reject/Cancel Transaction", tags=CRYPTO_TRANSACTION_TAGS)
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        with transaction.atomic():
            serializer = self.get_serializer(obj, data=request.data, partial=True, context={"user_id": request.user,
                                                                                            "is_moderator": self.is_moderator(
                                                                                                self.request)})
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({
            "result": "success",
            "object": TransactionSerializer(obj).data
        })


class CalculateWithdrawCommissionView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_id="Calculate Withdraw Commission",
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     required=["currency_code", 'network_code', 'amount'],
                                                     properties={
                                                         "currency_code": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                         title='Currency code'),
                                                         "network_code": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                        title='Network code'),
                                                         "amount": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                                  title='Amount'),
                                                     }))
    def post(self, request, *args, **kwargs):
        currency = get_object_or_404(BitPinCurrency, code=request.data.get("currency_code"))
        network = get_object_or_404(BitPinNetwork, code=request.data.get("network_code"))
        amount = request.data.get("amount")

        if not currency._has_network(network):
            raise CustomError(ERRORS.custom_message_error(
                _("Invalid network ID. Provided network must be present in currency networks.")))
        commission = currency.get_withdraw_commission_obj(network)
        amount_after_commission = currency.calculate_amount_after_withdraw_commission(amount, network)
        return Response({
            "result": "success",
            "amount": amount,
            "amount_after_commission": amount_after_commission,
            "commission": commission.amount,
            "commission_irt": commission.amount * currency.get_price(),
        })


calculate_commission = CalculateWithdrawCommissionView.as_view()


class OrderView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & OrderPermission)]

    def paginator(self):
        return False

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.is_moderator(self.request):
                return OrderForAdminSerializer
            return OrderSerializer
        return OrderCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Order List"), tags=ORDER_TAGS)
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "objects": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_id=_("Book a new Order"), tags=ORDER_TAGS)
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data, context={"user_id": self.request.user})
            serializer.is_valid(raise_exception=True)
            newb = serializer.save()
        return Response({
            "result": "success",
            "object": OrderSerializer(newb).data
        }, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & OrderPermission)]
    queryset = Order.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.is_moderator(self.request):
            return OrderForAdminSerializer
        return OrderSerializer

    @swagger_auto_schema(operation_id="Get Order Detail", tags=ORDER_TAGS)
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })


class CalculateOrderCommissionView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_id="Calculate BuySell Commission",
                         request_body=CalculateOrderCommissionSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CalculateOrderCommissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        currency = get_object_or_404(BitPinCurrency, code=request.data.get("currency_code"))
        amount = Decimal(request.data.get("amount"))
        cost = Decimal(request.data.get("cost"))
        _type = request.data.get("type")
        base_currency = get_object_or_404(BitPinCurrency, code=request.data.get("base_currency_code"))
        if cost and not amount:
            amount = cost / currency.get_price(base_currency.code)
        else:
            cost = amount * currency.get_price(base_currency.code)
        total = Order.get_amount_for_increase(_type, amount, currency, base_currency)
        comm = Order.get_commission_amount(currency, _type, amount, base_currency)
        return Response({
            "result": "success",
            "amount": amount,
            "current_price": currency.get_price(base_currency.code),
            "amount_after_commission": total - comm,
            "commission": comm,
            "cost": cost
        })


class TransferView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & OrderPermission)]

    def get_queryset(self):
        if self.is_moderator(self.request):
            return Transfer.objects.all()
        return Transfer.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransferSerializer
        return TransferCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Transfer List "), tags=TRANSFER_TAGS)
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "objects": self.get_serializer(self.get_queryset(), many=True).data
        })

    @swagger_auto_schema(operation_id=_("Create new Transfer "), tags=TRANSFER_TAGS)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({
            "result": "success",
            "object": TransferSerializer(instance).data
        })
