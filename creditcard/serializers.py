from PIL.ImageFile import ERRORS
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from creditcard.models import CreditCard
from exchange.error_codes import ERRORS
from jibit.models import JibitRequest
from users.serializer import UserSimplifiedSerializer


class CreditCardSerializer(serializers.ModelSerializer):
    user_id = UserSimplifiedSerializer()

    class Meta:
        model = CreditCard
        fields = "__all__"
        depth = 1


class CreditCardCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    iban = serializers.CharField()

    def create(self, validated_data):
        user = validated_data.get('user_id')
        instance = user.creditcard_set.create(card_number=validated_data.get('card_number'),
                                              iban=validated_data.get('iban'))
        JibitRequest.objects.create(user_id=user, type=JibitRequest.Type.NATIONAL_WITH_CARD).send_request(
            card_number=validated_data.get('card_number'), )
        JibitRequest.objects.create(user_id=user, type=JibitRequest.Type.NATIONAL_WITH_CARD).send_request(
            iban=validated_data.get('iban'))
        return instance

    def validate(self, attrs):
        user = self.context.get("user")
        card_number = attrs.get('card_number')
        iban = attrs.get('iban')
        if not user.mobile_matched_national_code:
            raise CustomError(ERRORS.custom_message_error(_("Your national code has not been approved yet.")))
        if not user.authority_option_ids.filter(field_key="birthdate").exists():
            raise CustomError(ERRORS.custom_message_error(_("Your birthdate has not been approved yet.")))
        if not card_number:
            raise CustomError(ERRORS.empty_field_error("card_number"))
        if len(card_number) != 16:
            raise CustomError(ERRORS.length_error("card_number", 16, 16))
        if not iban:
            raise CustomError(ERRORS.empty_field_error("iban"))
        if len(iban) != 26:
            raise CustomError(ERRORS.length_error("iban", 26, 26))

        if user.creditcard_set.filter(card_number=card_number, iban=iban).exists():
            raise CustomError(ERRORS.ERROR_DUPLICATE_CREDITCARD)

        return attrs


class CreditCardUpdateSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(min_length=16, max_length=16)
    iban = serializers.CharField(min_length=26, max_length=26)

    class Meta:
        model = CreditCard
        fields = ['card_number', 'iban']

    def update(self, instance, validated_data):
        instance.card_number = validated_data.get('card_number', instance.card_number)
        instance.iban = validated_data.get('iban', instance.iban)
        instance.approved = False
        instance.save()
        return instance
