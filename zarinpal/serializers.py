from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from zarinpal.models import RialDeposit, RialWithdraw


class RialDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialDeposit
        fields = ["id", "create_date", "write_date", "amount", "factor_number", "card_number", "status"]


class RialDepositAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialDeposit
        fields = '__all__'


class RialWithdrawCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=0, required=True)
    sheba_number = serializers.CharField(required=True, max_length=26)

    def validate(self, attrs):
        amount = attrs.get('amount')
        sheba_number = attrs.get('sheba_number')
        user_id = self.context.get("user_id")
        if not amount:
            raise CustomError(ERRORS.empty_field_error("amount"))
        if not sheba_number:
            raise CustomError(ERRORS.empty_field_error("sheba_number"))
        sheba = user_id.creditcard_set.filter(iban=sheba_number)
        if not sheba:
            raise CustomError(ERRORS.custom_message_error(_("Invalid sheba number")))
        if not sheba.first().approved:
            raise CustomError(ERRORS.custom_message_error(_("Sheba not approved.")))

        attrs["user_id"] = user_id
        return attrs

    def create(self, validated_data):
        return RialWithdraw.objects.create(**validated_data)


class RialWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialWithdraw
        fields = ["id", "create_date", "amount", "factor_number", "sheba_number", "status"]


class RialWithdrawAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = RialWithdraw
        fields = '__all__'


class ConfirmRialWithdrawSerializer(serializers.Serializer):
    withdraw_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=[('approve', _('Approve')), ('reject', _("Reject"))], required=True)

    def validate(self, attrs, *args, **kwargs):
        withdraw_id = attrs.get("withdraw_id")
        withdraw = get_object_or_404(RialWithdraw, pk=withdraw_id)
        if withdraw.status != withdraw.Status.PENDING:
            raise CustomError(_("Withdraw is not in pending state."))
        attrs["instance"] = withdraw
        return attrs

    def save(self, **kwargs):
        action = self.validated_data.get("action")
        instance = self.validated_data.get("instance")
        if action == 'approve':
            instance.confirm()
        else:
            instance.cancel()

        return instance