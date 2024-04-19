from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers import CustomModelSerializer
from authentication.exception import CustomError
from bitpin.models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress
from exchange.error_codes import ERRORS


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinNetwork
        exclude = ["create_date", "write_date"]


class CurrencySimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinCurrency
        fields = ["id", "code", "title", "title_fa", "image"]


class CurrencySerializer(CustomModelSerializer):
    networks = NetworkSerializer(many=True, source='network_ids')

    def __init__(self, *arg, **kwargs):
        fields = ["id", "title", "title_fa", "code", "image", "price", "price_info_change"]
        super().__init__(*arg, **kwargs)

        request = self.context.get("request")
        if fields and request and request.GET.get("for_dashboard") == 'true':
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = BitPinCurrency
        exclude = ["create_date", "write_date", "network_ids", "price_info_price"]
        depth = 2


class CurrencyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitPinCurrency
        fields = ["markup_percent", "bitasia_active", "buy_sell_commission", "buy_sell_commission_type"]


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

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=BitPinWalletAddress.objects.all(),
                fields=['currency_id', 'network_id']
            )
        ]

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
