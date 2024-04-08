from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from exchange.models import BaseModelWithDate

User = get_user_model()


class CreditCard(BaseModelWithDate):
    card_number = models.CharField(_('Credit card number'), max_length=16)
    iban = models.CharField(_("IBAN"), max_length=26)
    approved = models.BooleanField(_("Approved"), default=False)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Credit card")
        verbose_name_plural = _("Credit cards")

    def __str__(self):
        return self.card_number
