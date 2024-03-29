from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate


class BitPinNetwork(BaseModelWithDate):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255)


class BitPinCurrency(BaseModelWithDate):
    title = models.CharField(_("Title (English)"), max_length=255)
    title_fa = models.CharField(_("Title (فارسی)"), max_length=255, blank=True)
    code = models.CharField(_("Code"), max_length=10)
    image = models.URLField(_("Image URL"))
    min_withdraw = models.DecimalField(_("Minimum Withdrawal"), max_digits=10, decimal_places=2, blank=True,
                                       null=True)
    color = models.CharField(_("Color"), max_length=6)
    alias = models.CharField(_("Alias"), max_length=255, blank=True)
    withdraw_commission = models.DecimalField(_("Withdrawal Commission"), max_digits=10, decimal_places=8)
    withdraw_commission_type = models.CharField(_("Withdrawal Commission Type"), max_length=10)
    max_withdraw_commission = models.DecimalField(_("Maximum Withdrawal Commission"), max_digits=10,
                                                  decimal_places=8, blank=True, null=True)
    tradable = models.BooleanField(_("Tradable"))
    for_test = models.BooleanField(_("For Test"))
    decimal = models.IntegerField(_("Decimal Places"))
    decimal_amount = models.IntegerField(_("Decimal Amount"))
    decimal_irt = models.IntegerField(_("Decimal (IRT)"))
    high_risk = models.BooleanField(_("High Risk"))
    show_high_risk = models.BooleanField(_("Show High Risk"))
    recommend_for_deposit_weight = models.IntegerField(_("Recommend for Deposit Weight"))
    for_loan = models.BooleanField(_("For Loan"))
    for_stake = models.BooleanField(_("For Stake"))
    network_id = models.ManyToManyField(BitPinNetwork, )
    price_info_price = models.DecimalField(_("Price"), max_digits=20, decimal_places=8)
    price_info_time = models.DateTimeField(_("Time"))
    price_info_change = models.DecimalField(_("Change"), max_digits=10, decimal_places=4)
    price_info_min = models.DecimalField(_("Minimum"), max_digits=20, decimal_places=8)
    price_info_max = models.DecimalField(_("Maximum"), max_digits=20, decimal_places=8)
    price_info_mean = models.DecimalField(_("Mean"), max_digits=20, decimal_places=8)
    price_info_value = models.DecimalField(_("Market Value"), max_digits=20,
                                           decimal_places=8)  # Assuming value refers to market value
    price_info_amount = models.DecimalField(_("Market Amount"), max_digits=20, decimal_places=8)
    price_info_market_value = models.DecimalField(_("Total Market Value"), max_digits=20, decimal_places=8)
    price_info_market_amount = models.DecimalField(_("Total Market Amount"), max_digits=20, decimal_places=8)
    price_info_usdt_price = models.DecimalField(_("Price USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_time = models.DateTimeField(_("Time USDT"))
    price_info_usdt_change = models.DecimalField(_("Change USDT"), max_digits=10, decimal_places=4)
    price_info_usdt_min = models.DecimalField(_("Minimum USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_max = models.DecimalField(_("Maximum USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_mean = models.DecimalField(_("Mean USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_value = models.DecimalField(_("Market Value USDT"), max_digits=20,
                                                decimal_places=8)  # Assuming value refers to market value
    price_info_usdt_amount = models.DecimalField(_("Market Amount USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_market_value = models.DecimalField(_("Total Market Value USDT"), max_digits=20, decimal_places=8)
    price_info_usdt_market_amount = models.DecimalField(_("Total Market Amount USDT"), max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.title} ({self.title_fa})"

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
