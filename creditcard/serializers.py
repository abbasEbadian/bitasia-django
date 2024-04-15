from PIL.ImageFile import ERRORS
from rest_framework import serializers

from authentication.exception import CustomError
from creditcard.models import CreditCard
from exchange.error_codes import ERRORS
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

        new, created = user.creditcard_set.get_or_create(card_number=validated_data.get('card_number'),
                                                         iban=validated_data.get('iban'))
        if not created:
            raise CustomError(ERRORS.ERROR_DUPLICATE_CREDITCARD)
        return new

    def validate(self, attrs):
        card_number = attrs.get('card_number')
        iban = attrs.get('iban')

        if not card_number:
            raise CustomError(ERRORS.empty_field_error("card_number"))
        if len(card_number) != 16:
            raise CustomError(ERRORS.length_error("card_number", 16, 16))

        if not iban:
            raise CustomError(ERRORS.empty_field_error("iban"))

        if len(iban) != 26:
            raise CustomError(ERRORS.length_error("iban", 26, 26))

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
