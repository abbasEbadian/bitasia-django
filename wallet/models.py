from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate
from currency.models import Currency

User = get_user_model()


class Wallet(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    balance = models.FloatField(_('Balance'), default=0.0)

    def __str__(self):
        return f"{self.user_id.username} ({self.balance})"

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def get_balance(self):
        return self.balance

    def charge(self, amount: float):
        if amount < 0:
            if self.balance < amount:
                return False
            self.balance -= float(amount)
            self.save()
            return True

        self.balance += float(amount)
        self.save()
        return True
