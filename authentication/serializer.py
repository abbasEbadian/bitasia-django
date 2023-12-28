from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers


class OtpSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=[('mobile', 'mobile'), ('email', 'email')], required=True)
    mobile = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class AuthOtpSerializer(serializers.Serializer):

    mobile = serializers.CharField(
        label=_("Mobile"),
        trim_whitespace=True,
    )
    otp = serializers.CharField(
        label=_("OTP"),
    )

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        otp = attrs.get('otp')

        if mobile and otp:
            user = authenticate(request=self.context.get('request'), otp=otp, mobile=mobile)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "mobile" and "otp".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


