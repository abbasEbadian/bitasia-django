from django.shortcuts import get_object_or_404
from rest_framework import serializers

from bitpin.models import BitPinCurrency
from bitpin.serializers import CurrencySerializer
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    currency_id = CurrencySerializer()

    class Meta:
        model = Wallet
        exclude = ['create_date', 'write_date', 'user_id']


class WalletCreateSerializer(serializers.Serializer):
    currency_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        attrs["currency_id"] = get_object_or_404(BitPinCurrency, pk=attrs.get('currency_id'))
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user_id')
        currency = validated_data.get('currency_id')
        wallet = user.get_wallet(currency.code)
        return wallet

    def update(self, instance, validated_data):
        return super(WalletCreateSerializer, self).update(instance, validated_data)
