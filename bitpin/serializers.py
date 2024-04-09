from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from bitpin.models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress
from exchange.error_codes import ERRORS


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinNetwork
        exclude = ["create_date", "write_date"]


class CurrencySerializer(serializers.ModelSerializer):
    networks = NetworkSerializer(many=True, source='network_ids')

    class Meta:
        model = BitPinCurrency
        exclude = ["create_date", "write_date", "network_ids"]
        depth = 2


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


class WalletAddressCreateSerializer(serializers.Serializer):
    address = serializers.CharField(required=True)
    currency_id = serializers.IntegerField(required=True)
    network_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        currency = get_object_or_404(BitPinCurrency, pk=attrs.get("currency_id"))
        network = get_object_or_404(BitPinNetwork, pk=attrs.get("network_id"))
        if not currency._has_network(network):
            raise CustomError(ERRORS.custom_message_error(
                _("Invalid network ID. Provided network must be present in currency networks.")))
        attrs["currency"] = currency
        attrs["network"] = network
        return attrs

    def create(self, validated_data):
        return BitPinWalletAddress.objects.create(**{
            "currency_id": validated_data["currency"],
            "network_id": validated_data["network"],
            "address": validated_data["address"]
        })
