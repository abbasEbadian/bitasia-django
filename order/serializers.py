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
    type = serializers.ChoiceField(required=True, choices=Transaction.Type.choices)
    wallet_address = serializers.CharField(required=True, max_length=255)
    currency_id = serializers.IntegerField(required=True)
    network_id = serializers.IntegerField(required=True)
    amount = serializers.FloatField(required=True)
    tx_id = serializers.CharField(required=False)

    def validate(self, attrs, *args, **kwargs):
        currency = get_object_or_404(BitPinCurrency, pk=attrs.get("currency_id"))
        network = get_object_or_404(BitPinNetwork, pk=attrs.get("network_id"))
        if not currency._has_network(network):
            raise CustomError(
                ERRORS.custom_message_error(_("Provided network %s not present in currency networks.") % network.title))
        type = attrs.get('type')
        tx_id = attrs.get('tx_id')
        if type == Transaction.Type.DEPOSIT and not tx_id:
            raise CustomError(ERRORS.custom_message_error(_("tx_id is required for deposit. ")))

        if type == Transaction.Type.WITHDRAW:
            user = self.context.get('user_id')
            amount = attrs.get('amount')
            wallet = user.get_wallet(currency.code)
            print(wallet.balance, amount)
            if wallet.balance < amount:
                raise CustomError(ERRORS.custom_message_error(_("Insufficient balance.")))
        attrs["currency"] = currency
        attrs["network"] = network
        return attrs

    def create(self, validated_data, *args, **kwargs):
        currency_id = validated_data["currency"]
        network_id = validated_data["network"]
        user_id = self.context.get("user_id")
        amount = validated_data["amount"]
        type = validated_data["type"]
        tx_id = validated_data["tx_id"] if type == Transaction.Type.DEPOSIT else ""
        wallet_address = validated_data["wallet_address"]
        tr = Transaction.objects.create(**{
            "currency_id": currency_id,
            "network_id": network_id,
            "user_id": user_id,
            "tx_id": tx_id,
            "amount": amount,
            "status": Transaction.Status.PENDING,
            "type": type,
            "wallet_address": wallet_address,
            "currency_current_value": int(currency_id.price_info_price)
        })
        tr.after_create_request()
        return tr


class TransactionUpdateSerializer(serializers.Serializer):
    action = serializers.ChoiceField(required=True, choices=[
        ('accept', _("Accept")),
        ('reject', _("Reject")),
        ('cancel', _("Cancel")),
    ])
    tx_id = serializers.CharField()

    def validate(self, attrs, *args, **kwargs):
        if self.instance.status != Transaction.Status.PENDING:
            raise CustomError(
                ERRORS.custom_message_error(_("Cannot update transaction which is not in pending status.")))
        action = attrs.get('action')
        user = self.context.get("user_id")

        if action != "cancel":
            if not user.is_staff:
                raise PermissionError()
            if action == "accept":
                if not attrs.get('tx_id'):
                    raise CustomError(ERRORS.custom_message_error(_("Provide a tx_id for your transaction")))

        return attrs

    def update(self, instance, validated_attrs):
        action = validated_attrs.get('action')
        tx_id = validated_attrs.get('tx_id')
        if action == "accept":
            instance.tx_id = tx_id
            instance.approve()
        elif action == "reject":
            instance.reject()
        elif action == "cancel":
            instance.cancel()
        return instance
