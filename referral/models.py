from django.db import models
from django.utils.translation import gettext as _

from exchange.models import BaseModel


class ReferralProgram(BaseModel):
    min_subset_count = models.IntegerField()
    max_subset_count = models.IntegerField()
    percent = models.DecimalField(decimal_places=0, max_digits=3)

    class Meta:
        verbose_name = _('Referral Program')
        verbose_name_plural = _('Referral Programs')
