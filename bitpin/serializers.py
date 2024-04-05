from rest_framework import serializers

from bitpin.models import BitPinCurrency, BitPinNetwork


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinNetwork
        exclude = ["create_date", "write_date"]


class CurrencySerializer(serializers.ModelSerializer):
    networks = NetworkSerializer(many=True, source='network_ids')

    class Meta:
        model = BitPinCurrency
        exclude = ["create_date", "write_date", "network_ids"]
        depth = 1


class CurrencyDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinCurrency
        fields = ["id", "title", "title_fa", "code", "image", "price_info_price", "price_info_change"]
