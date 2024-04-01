from rest_framework import serializers

from bitpin.models import BitPinCurrency, BitPinNetwork


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinNetwork
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    networks = NetworkSerializer(many=True, source='network_ids')

    class Meta:
        model = BitPinCurrency
        fields = '__all__'
