from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from authentication.exception import CustomError
from bitpin.serializers import CurrencySerializer
from order.models import *
from users.serializer import UserSerializer


class OrderForAdminSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    currency_id = CurrencySerializer()

    class Meta:
        model = Order
        exclude = ["write_date"]
        depth = 2


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["write_date", "user_id"]
        depth = 2


class OrderCreateDepositSerializer(serializers.Serializer):
    currency_id = serializers.IntegerField(required=True)
    tx_id = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)

    def validate(self, attrs, *args, **kwargs):
        currency_id = attrs["currency_id"]
        user_id = self.context.get("user_id")
        tx_id = attrs["tx_id"]
        amount = attrs["amount"]
        order = Order.objects.create(**{
            "currency_id": BitPinCurrency.objects.get(pk=currency_id),
            "user_id": user_id,
            "tx_id": tx_id,
            "amount": amount,
            "status": PENDING,
            "type": DEPOSIT
        })
        attrs["order_id"] = order

        return attrs


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        exclude = ["write_date", "user_id"]
        depth = 1


class PurchaseCreateSerializer(serializers.Serializer):
    currency_id = serializers.IntegerField(required=True)
    amount = serializers.FloatField(required=True)

    def validate(self, attrs, *args, **kwargs):
        currency_id = attrs["currency_id"]
        amount = attrs["amount"]
        user_id = self.context.get("user_id")
        purchase = Purchase.objects.create(**{
            "currency_id": BitPinCurrency.objects.get(pk=currency_id),
            "user_id": user_id,
            "amount": amount,
            "status": PENDING
        })
        attrs["purchase_id"] = purchase
        return attrs


class PurchaseSubmitSerializer(serializers.Serializer):
    purchase_id = serializers.IntegerField(required=True)

    def validate(self, attrs, *args, **kwargs):
        purchase_id = attrs.get("purchase_id")
        purchase = get_object_or_404(Purchase, pk=purchase_id)
        if purchase.status != PENDING:
            raise CustomError(_("Purchase is not in pending state."))
        return attrs
