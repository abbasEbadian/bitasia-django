from django.db.transaction import atomic
from django.shortcuts import render
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.mixins import IsModeratorMixin
from api.permissions import IsModerator
from api.schema import create_payment_schema
from authentication.exception import CustomError
from authentication.models import OTP
from exchange.error_codes import ERRORS
from .models import RialDeposit, RialWithdraw
from .permissions import RialWithdrawPermission, RialDepositPermission
from .serializers import RialDepositAdminSerializer, RialDepositSerializer, RialWithdrawCreateSerializer, \
    RialWithdrawAdminSerializer, RialWithdrawSerializer, ConfirmRialWithdrawSerializer


class RialWithdrawView(generics.ListCreateAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(~IsModerator & IsAuthenticated) | (IsModerator & RialWithdrawPermission)]

    def paginator(self):
        return False

    def get_queryset(self):
        if self.is_moderator(self.request):
            return RialWithdraw.objects.all()
        return RialWithdraw.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            if self.is_moderator(self.request):
                return RialWithdrawAdminSerializer
            return RialWithdrawSerializer
        return RialWithdrawCreateSerializer

    @swagger_auto_schema(operation_id=_("Get Rial withdraw list"), tags=["Transactions - Rial"])
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "object": serializer.data
        })

    @swagger_auto_schema(operation_id=_("Create new withdraw"), tags=["Transactions - Rial"])
    def post(self, request, *args, **kwargs):
        with atomic():
            serializer = self.get_serializer(data=request.data, context={"user_id": request.user})
            serializer.is_valid(raise_exception=True)
            withdraw = serializer.save()
            withdraw.submit()

            return Response({
                "result": "success",
                "object": RialWithdrawSerializer(withdraw).data
            }, status=status.HTTP_201_CREATED)


class RialWithdrawConfirmView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsModerator]
    serializer_class = ConfirmRialWithdrawSerializer
    http_method_names = ["patch"]

    @swagger_auto_schema(operation_id=_("Approve or reject withdraw"), tags=["Transactions - Rial"])
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "success",
            "message": _("Submitted successfully")
        })


class RialDepositView(generics.ListAPIView, IsModeratorMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(IsAuthenticated & ~IsModerator) | (IsModerator & RialDepositPermission)]

    def paginator(self):
        return False

    def get_queryset(self):
        if self.is_moderator(self.request):
            return RialDeposit.objects.all()
        return RialDeposit.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.is_moderator(self.request):
            return RialDepositAdminSerializer
        return RialDepositSerializer

    @swagger_auto_schema(operation_id=_("Get Rial deposit list"), tags=["Transactions - Rial"])
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "result": "success",
            "object": serializer.data
        })


@swagger_auto_schema(**create_payment_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_rial_deposit(request):
    user = request.user
    data = request.data
    amount = data.get('amount', 0)
    card_number = data.get('card_number')
    try:
        amount = int(amount)
        if not amount or amount < 10000:
            raise CustomError(ERRORS.ERROR_INVALID_AMOUNT)

        card = user.creditcard_set.filter(card_number=card_number)

        if not card_number or not card.exists() or not card.first().approved:
            raise CustomError(ERRORS.ERROR_INVALID_CARD)

        deposit = RialDeposit.objects.create(user_id=user, amount=amount, card_number=card_number)
        result = deposit.create_payment()
        if result:
            return Response({
                "result": "success",
                "url": result
            })

    except Exception as e:
        raise CustomError(ERRORS.ERROR_GATEWAY)


@swagger_auto_schema(auto_schema=None, method="GET")
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def payment_callback(request):
    authority = request.query_params.get('Authority')
    _status = request.query_params.get('Status', [])
    transaction = RialDeposit.objects.filter(gateway_token=authority).first()
    message = ""
    success = True
    transaction_is_valid = False

    if transaction is None:
        message = _("Transaction not found")
        success = False

    if success and not transaction.is_pending():
        message = _("Transaction has been already checked")
        success = False

    if success and "NOK" in _status:
        message = _("Transaction Failed")
        success = False

    if success:
        transaction_is_valid = transaction.check_transaction_integrity()

    if success and not transaction_is_valid:
        success = False
        message = _("Transaction Failed")

    if success and "OK" in _status:
        message = _("Transaction successful")

    if not transaction:
        return Response({
            "result": success and "success" or "error",
            "message": message
        })
    if not success:
        transaction.cancel()
    else:
        transaction.success()

    return render(request, "zarinpal/payment_callback.html", {
        "success": success,
        "message": message,
        "card_number": transaction.card_number,
        "amount": f"{transaction.amount:,}",
        "factor_number": transaction.factor_number,
        "ref_id": transaction.verifyline_set.last() and transaction.verifyline_set.last().ref_id
    })


@swagger_auto_schema(operation_id=_("Send otp for Rial Withdrawal"), method="POST", tags=["Transactions - Rial"])
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_rial_withdraw_otp(request):
    user = request.user
    instance = user.send_otp(OTP.Type.WITHDRAW)
    if instance:
        return Response({
            "result": "success",
            "message": _("OTP sent successfully")
        }, status=status.HTTP_201_CREATED)
    return Response({
        "result": "error",
        "message": _("Unable to connect to the SMS service provider at the moment.")
    })
