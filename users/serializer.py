from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from authentication.models import OTP
from authority.models import get_user_level
from exchange.error_codes import ERRORS
from wallet.serializers import WalletSerializer

User = get_user_model()


class UserSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions']


class UserSerializer(serializers.ModelSerializer):
    user_level = serializers.SerializerMethodField('_get_user_level')
    approved_rule_ids = serializers.SerializerMethodField('_approved_rule_ids')
    authentication_status = serializers.SerializerMethodField('_authentication_status')
    wallets = serializers.SerializerMethodField('_wallets')
    total_ir_balance = serializers.SerializerMethodField("_total_balance")

    def _get_user_level(self, obj):
        return get_user_level(obj)

    def _approved_rule_ids(self, obj):
        return [x.rule_id.id for x in obj.authorityrequest_set.filter(approved=True)]

    def _wallets(self, obj):
        return WalletSerializer(obj.wallet_set.all(), many=True).data

    def _authentication_status(self, obj):
        return obj.authorityrequest_set.filter(
            approved=False).count() > 0 and "pending" or f"level_{self._get_user_level(obj)}"

    def _total_balance(self, obj):
        total = float(0)
        for wallet in obj.wallet_set.all():
            if wallet.currency_id.code == "IRT":
                total += wallet.balance
            else:
                total += wallet.currency_id.price_info_price * wallet.balance

        return total

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


class VerifyForgetPasswordSerializer(serializers.Serializer):
    password_1 = serializers.CharField(required=True, min_length=6)
    password_2 = serializers.CharField(required=True)
    otp = serializers.CharField(required=True, min_length=5, max_length=5)
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate(self, attrs):
        password_1 = attrs.get('password_1')
        password_2 = attrs.get('password_2')
        mobile = attrs.get('mobile')
        _otp = attrs.get('otp')
        user = User.objects.filter(mobile=mobile)
        if not user.exists():
            raise CustomError(ERRORS.custom_message_error(_("User not found.")))
        if password_1 != password_2:
            raise CustomError(ERRORS.custom_message_error(_("Passwords doesn't match.")))
        user = user.first()
        otp = OTP.objects.filter(user_id=user, code=_otp, type=OTP.Type.FORGET_PASSWORD)
        if not otp.exists():
            raise CustomError(ERRORS.custom_message_error(_("Wrong OTP.")))
        attrs["otp_id"] = otp.first()
        attrs["user"] = user

        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        password = validated_data.get("password_1")
        otp = validated_data["otp_id"]
        otp.consume()
        user.set_password(password)
        user.save(update_fields=["password"])
        return otp


class ForgetPasswordSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, min_length=11, max_length=11)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        user = User.objects.filter(mobile=mobile)
        if not user.exists():
            raise CustomError(ERRORS.custom_message_error(_("User not found.")))
        attrs["user"] = user.first()
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        otp = user.send_otp(otp_type=OTP.Type.FORGET_PASSWORD)
        return otp
