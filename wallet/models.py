from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from authentication.exception import CustomError
from bitpin.models import BitPinCurrency
from exchange.error_codes import ERRORS
from exchange.models import BaseModelWithDate

User = get_user_model()


class Wallet(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(_('Balance'), default=0.0, decimal_places=11, max_digits=24)

    def __str__(self):
        return f"{self.user_id.username} ({self.balance})"

    class Meta:
        ordering = ('-balance',)
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def get_balance(self):
        return self.balance

    def charge(self, amount):
        if amount < 0:
            if self.balance < amount:
                raise CustomError(ERRORS.custom_message_error(_("Insufficient balance.")))
            self.balance += Decimal(amount)
            self.save()
            return True

        self.balance += Decimal(amount)
        self.save()
        return True
