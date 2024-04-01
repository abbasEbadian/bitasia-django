from rest_framework import serializers

from bitpin.serializers import CurrencySerializer
from order.models import Order
from users.serializer import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    currency_id = CurrencySerializer()

    class Meta:
        model = Order
        exclude = ["create_date", "write_date"]
        depth = 1
