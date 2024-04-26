from django.utils.translation import gettext as _
from rest_framework import serializers

from authentication.exception import CustomError
from exchange.error_codes import ERRORS
from referral.models import ReferralProgram


class ReferralProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralProgram
        fields = '__all__'


class ReferralProgramCreateSerializer(serializers.Serializer):
    min_subset_count = serializers.IntegerField(required=True)
    max_subset_count = serializers.IntegerField(required=True)
    percent = serializers.DecimalField(max_digits=3, decimal_places=0, min_value=0, max_value=100, required=True)

    def validate(self, attrs):
        min_subset_count = attrs.get('min_subset_count')
        max_subset_count = attrs.get('max_subset_count')
        if min_subset_count > max_subset_count:
            max_subset_count, min_subset_count = min_subset_count, max_subset_count
        qs = ReferralProgram.objects.all().order_by("min_subset_count")
        if hasattr(self, "instance") and self.instance is not None: qs = qs.filter(pk=self.instance.id)
        for ref in qs:
            if min_subset_count <= ref.min_subset_count <= max_subset_count:
                raise CustomError(ERRORS.custom_message_error(_("This program has overlapped with another program.")))
        return attrs

    def create(self, validated_data):
        return ReferralProgram.objects.create(**validated_data)

    def update(self, instance, validated_data):
        ref = ReferralProgram.objects.filter(pk=instance.pk)
        ref.update(**validated_data)
        return ref.first()
