from django.db import models
from django.utils.translation import gettext as _

from bitpin.models import BitPinCurrency, BitPinNetwork
from exchange.models import BaseModelWithDate


class WithdrawCommission(BaseModelWithDate):
    class CommissionType(models.TextChoices):
        VALUE = 'value', _("Value")
        PERCENT = "percent", _("Percent")

    currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.CASCADE)
    network_id = models.ForeignKey(BitPinNetwork, on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Commission Type"), choices=CommissionType.choices,
                            default=CommissionType.VALUE)
    amount = models.FloatField(verbose_name=_("Commission Amount"), default=0)

    def __str__(self):
        return f"{self.amount} of {self.type} ({self.currency_id.code}:{self.network_id.code})"

    class Meta:
        verbose_name = _("Withdraw Commission")
        verbose_name_plural = _("Withdraw Commissions")

        constraints = [
            models.UniqueConstraint(fields=['currency_id', 'network_id'], name='currency_network_id')
        ]
