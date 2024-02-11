from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.schema import create_payment_schema
from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from .models import RialDeposit


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
        int(amount)
        amount = int(amount)
        if not amount or amount < 1000:
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
    except CustomError as c:
        raise c

    except Exception as e:
        raise CustomError(ERRORS.ERROR_GATEWAY)


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
            "result": success,
            "message": message
        })
    if not success:
        transaction.cancel()
    else:
        transaction.success()

    return Response({
        "result": success,
        "message": message
    })