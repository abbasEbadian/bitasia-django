from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from bitpin.serializers import CurrencySerializer, CurrencySimplifiedSerializer
from exchange.error_codes import ERRORS
from order.models import *
from users.serializer import UserSerializer, UserSimplifiedSerializer


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
    amount = serializers.FloatField(required=True, min_value=0)
    tx_id = serializers.CharField(required=False)

    def validate(self, attrs, *args, **kwargs):
        currency = get_object_or_404(BitPinCurrency, pk=attrs.get("currency_id"))
        network = get_object_or_404(BitPinNetwork, pk=attrs.get("network_id"))
        amount = attrs.get("amount")

        if amount < currency.min_withdraw:
            raise CustomError(ERRORS.custom_message_error("Min withdraw is %d." % currency.min_withdraw))
        if not currency._has_network(network):
            raise CustomError(
                ERRORS.custom_message_error(_("Provided network %s not present in currency networks.") % network.title))

        amount_after_commission = currency.calculate_amount_after_commission(amount=amount, network=network)

        type = attrs.get('type')
        tx_id = attrs.get('tx_id')
        if type == Transaction.Type.DEPOSIT and not tx_id:
            raise CustomError(ERRORS.custom_message_error(_("tx_id is required for deposit. ")))

        if type == Transaction.Type.WITHDRAW:
            user = self.context.get('user_id')
            amount = amount_after_commission
            wallet = user.get_wallet(currency.code)
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
        amount_after_commission = currency_id.calculate_amount_after_commission(amount=amount, network=network_id)
        tr = Transaction.objects.create(**{
            "currency_id": currency_id,
            "network_id": network_id,
            "user_id": user_id,
            "tx_id": tx_id,
            "amount": amount_after_commission,
            "status": Transaction.Status.PENDING,
            "type": type,
            "wallet_address": wallet_address,
            "currency_current_value": int(currency_id.price_info_price)
        })
        if type == Transaction.Type.WITHDRAW:
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
        depth = 1


class OrderCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=Order.Type.choices)
    currency_id = serializers.IntegerField(required=True)
    amount = serializers.FloatField(required=True)

    def validate(self, attrs, *args, **kwargs):
        currency = get_object_or_404(BitPinCurrency, pk=attrs.get("currency_id"))
        user = self.context.get('user_id')
        amount = attrs.get('amount')
        type = attrs.get('type')
        wallet = user.get_wallet(currency.code)
        if type == Order.Type.BUY:
            amount *= currency.price_info_price
            wallet = user.get_wallet("IRT")
        if wallet.balance < amount:
            raise CustomError(ERRORS.custom_message_error(_("Insufficient balance.")))
        attrs["currency"] = currency
        attrs["user"] = user
        return attrs

    def create(self, validated_data, *args, **kwargs):
        currency_id = validated_data["currency"]
        user_id = validated_data["user"]
        amount = validated_data["amount"]
        type = validated_data["type"]
        order = Order.objects.create(**{
            "currency_id": currency_id,
            "user_id": user_id,
            "amount": amount,
            "status": Order.Status.PENDING,
            "type": type,
            "currency_current_value": int(currency_id.price_info_price)
        })
        order.after_create_request()
        order.approve()
        return order


class TransferSerializer(serializers.ModelSerializer):
    currency_id = CurrencySimplifiedSerializer()
    user_id = UserSimplifiedSerializer()

    class Meta:
        model = Transfer
        fields = "__all__"
        depth = 1


class TransferCreateSerializer(serializers.Serializer):
    currency_code = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True, min_value=0)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate(self, attrs, *args, **kwargs):
        currency = get_object_or_404(BitPinCurrency, code=attrs.get("currency_code"))
        mobile = attrs.get("mobile")
        amount = attrs.get("amount")
        user = self.context.get('request').user

        wallet = user.has_wallet(currency.code)
        if not wallet or user.get_wallet(currency.code).balance < amount:
            raise CustomError(ERRORS.custom_message_error(_("Insufficient balance.")))

        dest_user = User.objects.filter(mobile=mobile).first()
        if not dest_user:
            raise CustomError(ERRORS.custom_message_error(_("Destination user does not exist.")))
        attrs["currency_id"] = currency
        attrs["user_id"] = user
        attrs["dest_user_id"] = dest_user
        return attrs

    def create(self, validated_data, *args, **kwargs):
        currency_id = validated_data["currency_id"]
        mobile = validated_data["mobile"]
        amount = validated_data["amount"]
        user = validated_data["user_id"]
        dest_user = validated_data["dest_user_id"]
        with atomic():
            wallet_1 = user.get_wallet(currency_id.code)
            wallet_2 = dest_user.get_wallet(currency_id.code)
            new_transfer = Transfer.objects.create(**{
                "currency_id": currency_id,
                "user_id": user,
                "destination_mobile": mobile,
                "amount": amount,
                "successful": False
            })
            wallet_1.charge(-1 * amount)
            wallet_2.charge(amount)
            new_transfer.successful = True
            new_transfer.save()
            return new_transfer
