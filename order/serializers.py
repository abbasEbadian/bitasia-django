from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from bitpin.serializers import CurrencySerializer
from exchange.error_codes import ERRORS
from order.models import *
from users.serializer import UserSerializer


class TransactionForAdminSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    currency_id = CurrencySerializer()

    class Meta:
        model = Transaction
        exclude = ["write_date"]
        depth = 2


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["write_date", "user_id"]
        depth = 1


class TransactionCreateSerializer(serializers.Serializer):
    currency_id = serializers.IntegerField(required=True)
    tx_id = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    type = serializers.ChoiceField(required=True, choices=Transaction.Type.choices)
    wallet_address = serializers.CharField(max_length=255)
    network_id = serializers.IntegerField(required=True)

    def validate(self, attrs, *args, **kwargs):
        network_id = attrs["network_id"]
        currency_id = attrs["currency_id"]

        currency = get_object_or_404(currency_id)
        network = get_object_or_404(network_id)
        if not currency.netword_ids.filter(id=network.id):
            raise CustomError(
                ERRORS.custom_message_error(_("Provided network %s not present in currency networks.") % network.title))

        return attrs

    def create(self, validated_data, *args, **kwargs):
        currency_id = validated_data["currency_id"]
        network_id = validated_data["network_id"]
        user_id = self.context.get("user_id")
        tx_id = validated_data["tx_id"]
        amount = validated_data["amount"]
        type = validated_data["type"]
        wallet_address = validated_data["wallet_address"]
        return Transaction.objects.create(**{
            "currency_id": BitPinCurrency.objects.get(pk=currency_id),
            "user_id": user_id,
            "tx_id": tx_id,
            "amount": amount,
            "status": Transaction.Status.PENDING,
            "type": type,
            "wallet_address": wallet_address,
            "network_id": BitPinNetwork.objects.get(pk=network_id)
        })

# class PurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Purchase
#         exclude = ["write_date", "user_id"]
#         depth = 1
#
#
# class PurchaseCreateSerializer(serializers.Serializer):
#     currency_id = serializers.IntegerField(required=True)
#     amount = serializers.FloatField(required=True)
#
#     def validate(self, attrs, *args, **kwargs):
#         currency_id = attrs["currency_id"]
#         amount = attrs["amount"]
#         user_id = self.context.get("user_id")
#         purchase = Purchase.objects.create(**{
#             "currency_id": BitPinCurrency.objects.get(pk=currency_id),
#             "user_id": user_id,
#             "amount": amount,
#             "status": PENDING
#         })
#         attrs["purchase_id"] = purchase
#         return attrs
#
#
# class PurchaseSubmitSerializer(serializers.Serializer):
#     purchase_id = serializers.IntegerField(required=True)
#
#     def validate(self, attrs, *args, **kwargs):
#         purchase_id = attrs.get("purchase_id")
#         purchase = get_object_or_404(Purchase, pk=purchase_id)
#         if purchase.status != PENDING:
#             raise CustomError(_("Purchase is not in pending state."))
#         return attrs
