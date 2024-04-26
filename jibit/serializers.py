from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from jibit.models import JibitRequest

User = get_user_model()


class JibitSerializer(serializers.ModelSerializer):
    class Meta:
        model = JibitRequest
        fields = '__all__'
        depth = 1


class JibitCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    type = serializers.ChoiceField(choices=JibitRequest.Type.choices, required=True)
    card_number = serializers.CharField(required=False)
    iban = serializers.CharField(required=False)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        card_number = attrs.get('card_number')
        iban = attrs.get('iban')
        type = attrs.get('type')
        user = get_object_or_404(User, id=user_id)
        if type == JibitRequest.Type.NATIONAL_WITH_CARD:
            if not card_number and not iban:
                raise CustomError(ERRORS.custom_message_error(_("Either card_number or iban must be provided")))
            if card_number and iban:
                raise CustomError(ERRORS.custom_message_error(_("Request for Card number and IBAN separately")))
        else:
            if not user_id.national_code:
                raise CustomError(ERRORS.custom_message_error(_("Specified user has no national code.")))

        attrs["user"] = user
        return attrs

    def create(self, attrs):
        user_id = attrs.get('user')
        type = attrs.get('type')
        iban = attrs.get('iban')
        card_number = attrs.get('card_number')
        instance = JibitRequest.objects.create(user_id=user_id, type=type)
        instance.send_request(card_number, iban)
        return instance
