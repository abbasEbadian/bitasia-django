from rest_framework import serializers

from bitpin.models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress


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


class WalletAddressSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    network = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BitPinWalletAddress
        fields = ["id", "address", "currency", "network"]
        depth = 1

    def get_currency(self, obj):
        return obj.currency_id.code

    def get_network(self, obj):
        return f"{obj.network_id.code}({obj.network_id.title})"

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address")
        instance.save()
        return instance
