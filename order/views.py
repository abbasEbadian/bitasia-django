from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.permissions import IsOwner
from order.models import Transaction
from order.serializers import TransactionSerializer, TransactionForAdminSerializer, TransactionCreateSerializer, \
    TransactionUpdateSerializer

CRYPTO_TRANSACTION_TAGS = ["Transactions - Crypto"]


class TransactionView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def paginator(self):
        return False

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.request.user.is_staff:
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
        serializer = self.get_serializer(data=request.data, context={"user_id": self.request.user})
        serializer.is_valid(raise_exception=True)
        newb = serializer.save()
        return Response({
            "result": "success",
            "object": TransactionSerializer(newb).data
        }, status=status.HTTP_201_CREATED)


class TransactionDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsOwner | IsAdminUser]
    queryset = Transaction.objects.all()
    lookup_field = "id"
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.request.user.is_staff:
                return TransactionForAdminSerializer
            return TransactionSerializer
        return TransactionUpdateSerializer

    @swagger_auto_schema(operation_id="Get Transaction Detail", tags=CRYPTO_TRANSACTION_TAGS)
    def get(self, request, *args, **kwargs):
        return Response({
            "result": "success",
            "object": self.get_serializer(self.get_object()).data
        })

    @swagger_auto_schema(operation_id="Accept/Reject/Cancel Transaction", tags=CRYPTO_TRANSACTION_TAGS)
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data, partial=True, context={"user_id": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "success",
            "object": TransactionSerializer(obj).data
        })

# class PurchaseView(generics.ListCreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = []
#
#     def paginator(self):
#         return False
#
#     def get_queryset(self):
#         return Purchase.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method.lower() == 'get':
#             return PurchaseSerializer
#         return PurchaseCreateSerializer
#
#     @swagger_auto_schema(operation_id=_("Get Purchase List"))
#     def get(self, request):
#         serializer = PurchaseSerializer(self.get_queryset(), many=True)
#         return Response({
#             "result": "success",
#             "objects": serializer.data
#         }, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(operation_id=_("Create new purchase"))
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={"user_id": request.user})
#         serializer.is_valid(raise_exception=True)
#         valid_attrs = serializer.validated_data
#         return Response({
#             "result": "success",
#             "object": PurchaseSerializer(valid_attrs["purchase_id"]).data
#         }, status=status.HTTP_201_CREATED)
#
#
# class PurchaseAdminConfirmView(generics.UpdateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = [CanConfirmPurchase]
#     serializer_class = PurchaseSubmitSerializer
#     http_method_names = ["patch"]
#
#     @swagger_auto_schema(operation_id=_("Submit a purchase"))
#     def patch(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=False)
#         purchase = serializer.validated_data["purchase_id"]
#         result, message = purchase.confirm()
#         return Response({
#             "result": result,
#             "message": message
#         })
