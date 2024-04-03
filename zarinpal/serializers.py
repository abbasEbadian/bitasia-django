from rest_framework import serializers

from zarinpal.models import RialDeposit


class RialDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialDeposit
        fields = ["id", "create_date", "write_date", "amount", "factor_number", "card_number", "status"]


class RialDepositAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialDeposit
        fields = '__all__'
