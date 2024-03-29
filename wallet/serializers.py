from rest_framework import serializers

from bitpin.models import BitPinCurrency
from wallet.models import Wallet


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinCurrency
        exclude = ['create_date', 'write_date']


class WalletSerializer(serializers.ModelSerializer):
    currency_id = CurrencySerializer()

    class Meta:
        model = Wallet
        exclude = ['create_date', 'write_date', 'user_id']
