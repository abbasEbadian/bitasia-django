from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate
from bitpin.models import BitPinCurrency

User = get_user_model()

DEPOSIT = "deposit"
DEPOSIT_LABEL = _("Deposit")
WITHDRAWAL = "withdrawal"
WITHDRAWAL_LABEL = _("Withdrawal")

# States
PENDING = "pending"
PENDING_LABEL = _("Pending")
CANCEL = "cancel"
CANCEL_LABEL = _("Cancel")
SUCCESS = "success"
SUCCESS_LABEL = _("Success")


class Order(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.RESTRICT)
    type = models.CharField(max_length=10, choices=[
        (DEPOSIT, DEPOSIT_LABEL),
        (WITHDRAWAL, WITHDRAWAL_LABEL),
    ])
    status = models.CharField(max_length=10, choices=[
        (PENDING, PENDING_LABEL),
        (CANCEL, CANCEL_LABEL),
        (SUCCESS, SUCCESS_LABEL)
    ])
    tx_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"))
    amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name=_("Amount"))

    def __str__(self):
        return f"{self.type} / {self.amount} {self.currency_id.code} / {self.user_id.username}"

    class Meta:
        ordering = ('-id',)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
