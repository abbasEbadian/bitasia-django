from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from authentication.exception import CustomError
from bitpin.models import BitPinCurrency, BitPinNetwork
from commission.models import WithdrawCommission
from exchange.error_codes import ERRORS

COMM_TYPES = [
    ('value', 'Value'),
    ('percent', 'Percent'),
]


class WithdrawCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawCommission
        fields = '__all__'
        depth = 1


class WithdrawCommissionCreateSerializer(serializers.Serializer):
    currency_code = serializers.CharField(required=True)
    network_code = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    type = serializers.ChoiceField(required=True, choices=COMM_TYPES)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=WithdrawCommission.objects.all(),
                fields=['currency_id', 'network_id']
            )
        ]

    def validate(self, attrs):
        currency = get_object_or_404(BitPinCurrency, code=attrs.get('currency_code'))
        network = get_object_or_404(BitPinNetwork, code=attrs.get('network_code'))
        if not currency._has_network(network):
            raise CustomError(ERRORS.custom_message_error(
                _("Invalid network ID. Provided network must be present in currency networks.")))
        attrs["currency_id"] = currency
        attrs["network_id"] = network
        return attrs

    def create(self, validated_data):
        fields = ["currency_id", "network_id", "amount", "type"]
        return WithdrawCommission.objects.create(**{f: validated_data[f] for f in fields})


class WithdrawCommissionUpdateSerializer(serializers.Serializer):
    amount = serializers.FloatField(required=True, min_value=0)
    type = serializers.ChoiceField(required=True, choices=COMM_TYPES)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount')
        instance.type = validated_data.get('type')
        return instance
