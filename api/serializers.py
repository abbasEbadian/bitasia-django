from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class ShortDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        return super().to_representation(value).rstrip('0').rstrip('.')


class CustomModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        **ModelSerializer.serializer_field_mapping,
        models.DecimalField: ShortDecimalField,
    }
