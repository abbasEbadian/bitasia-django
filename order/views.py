from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.schema import create_payment_schema
from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from order.models import RialDeposit


@swagger_auto_schema(**create_payment_schema)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_rial_deposit(request):
    user = request.user
    data = request.data
    amount = int(data['amount'])
    card_number = data['card_number']

    if not amount or amount < 1000:
        raise CustomError(ERRORS.ERROR_INVALID_AMOUNT)

    card = user.creditcard_set.filter(card_number=card_number)
    if not card_number or not card.exists() or not card.first().approved:
        raise CustomError(ERRORS.ERROR_INVALID_CARD)

    deposit = RialDeposit.objects.create(user_id=user, amount=amount * 10, card_number=card_number)
    result = deposit.create_payment()
    if result:
        return Response({
            "result": "success",
            "url": result
        })


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def payment_callback(request):
    print(request.data)
    print(request.query_params)
    return Response(data=request.data)
