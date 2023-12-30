import re

from django.utils.translation import gettext as _
from rest_framework import serializers


class MobileValidator:
    def __init__(self, base=""):
        self.base = base

    def __call__(self, value):
        pattern = re.compile(r"^09\d{9}$")
        if not pattern.match(value):
            message = _('This value is invalid')
            raise serializers.ValidationError(message)
        return True
