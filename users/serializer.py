from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

from authority.models import get_user_level
from wallet.serializers import WalletSerializer

User = get_user_model()


class UserSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'is_active']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "content_type_id"]
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cid = data.pop("content_type_id")
        data["category"] = ContentType.objects.get(pk=cid).model
        return data


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    user_level = serializers.SerializerMethodField('_get_user_level')
    approved_rule_ids = serializers.SerializerMethodField('_approved_rule_ids')
    authentication_status = serializers.SerializerMethodField('_authentication_status')
    wallets = serializers.SerializerMethodField('_wallets')
    total_ir_balance = serializers.SerializerMethodField("_total_balance")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context.get("is_moderator"):
            return ret
        ret["groups"] = GroupSerializer(instance.groups.all(), many=True).data
        ret["user_permissions"] = PermissionSerializer(instance.user_permissions.all(), many=True).data
        return ret

    def _get_user_level(self, obj):
        return get_user_level(obj)

    def _approved_rule_ids(self, obj):
        return [x.rule_id.id for x in obj.authorityrequest_set.filter(approved=True)]

    def _wallets(self, obj):
        return WalletSerializer(obj.wallets.all(), many=True).data

    def _authentication_status(self, obj):
        return obj.authorityrequest_set.filter(
            approved=False).count() > 0 and "pending" or f"level_{self._get_user_level(obj)}"

    def _total_balance(self, obj):
        total = Decimal(0)
        for wallet in obj.wallets.all():
            if wallet.currency_id.code == "IRT":
                total += Decimal(wallet.balance)
            else:
                total += Decimal(wallet.currency_id.get_price()) * Decimal(wallet.balance)

        return total

    class Meta:
        model = User
        fields = ("__all__")
        depth = 1


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


class UserUpdateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)
    groups = serializers.CharField(help_text=_('Comma separated list of groups'), required=False)

    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', None)
        is_staff = validated_data.get('is_staff', None)
        _groups = validated_data.get('groups', None)
        if is_active is not None:
            instance.is_active = is_active
        if is_staff is not None:
            instance.is_staff = is_staff
        _groups = [x.strip() for x in _groups.split(",")]
        groups = Group.objects.filter(name__in=_groups)
        print(groups)
        instance.groups.set(groups)
        instance.save()
        return instance
