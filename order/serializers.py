from rest_framework import serializers

from bitpin.models import BitPinCurrency
from bitpin.serializers import CurrencySerializer
from users.serializer import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    currency_id = CurrencySerializer()

    class Meta:
        model = BitPinCurrency
        exclude = ["create_date", "write_date"]
        depth = 1
