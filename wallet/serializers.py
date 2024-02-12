from rest_framework import serializers

from wallet.models import Currency, Wallet


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ['create_date', 'write_date']


class WalletSerializer(serializers.ModelSerializer):
    currency_id = CurrencySerializer()

    class Meta:
        model = Wallet
        exclude = ['create_date', 'write_date', 'user_id']
