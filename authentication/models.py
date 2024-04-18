from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext as _

from exchange import settings
from exchange.models import BaseModelWithDate

User = get_user_model()


class OTP(BaseModelWithDate):
    class Type(models.TextChoices):
        LOGIN = "login", _("Login")
        WITHDRAW = "withdraw", _("Withdraw")
        TRANSFER = "transfer", _("Transfer")
        RESET_PASSWORD = "reset_password", _("Reset Password")
        FORGET_PASSWORD = "forget_password", _("Forget Password")

    code = models.IntegerField(verbose_name=_("Code"), blank=False)
    user_id = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    type = models.CharField(max_length=20, default=Type.LOGIN, choices=Type.choices)
    consumed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    def consume(self):
        self.consumed = True
        self.save()

    def expire(self):
        self.expired = True
        self.save(update_fields=["expired"])

    def has_expired(self):
        if self.expired: return True
        now = datetime.now()
        return (now - self.create_date).seconds // 60 > settings.OTP_EXPIRE_MINUTES

    def __str__(self):
        return f"{self.code}({self.type}) | {self.consumed and 'consumed' or ''} {self.expired and 'expired' or ''}"
