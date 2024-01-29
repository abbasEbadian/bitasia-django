from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate

User = get_user_model()


def get_file_path_for_icon(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/avatars/%s.%s" % (instance.name, ext)
    return filename


class Currency(BaseModelWithDate):
    name = models.CharField(_('Name'))
    symbol = models.CharField(_('Symbol'))
    icon = models.ImageField(_('Icon'), upload_to=get_file_path_for_icon)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class Wallet(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    balance = models.FloatField(_('Balance'), default=0.0)

    def __str__(self):
        return f"{self.user_id.name} ({self.balance})"

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def get_balance(self):
        return self.balance

    def modify_balance(self, amount: float):
        if amount < 0:
            if self.balance < amount:
                return False
            self.balance -= amount
            return True

        self.balance += amount
        return True
