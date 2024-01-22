from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile', 'username', 'is_staff', 'first_name', 'last_name', 'email',)
        extra_kwargs = {
            'mobile': {'required': True, 'help_text': "09876543210",
                       'validators': [MinLengthValidator(11), MaxLengthValidator(11)]},
            'email': {'validators': [EmailValidator()]},
            'username': {'required': True}, 'is_staff': {'default': False}}

    def validate(self, data):
        mobile = data.get('mobile')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        is_staff = data.get('is_staff', False)

        if not mobile or not username:
            raise serializers.ValidationError(_('Must provide mobile number.'))
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'gender', 'birthdate',
                  'national_card_image', 'birth_card_image', 'avatar_image')
