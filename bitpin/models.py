from django.db import models
from django.utils.translation import gettext as _

from authority.models import BaseModelWithDate


class BitPinNetwork(BaseModelWithDate):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} : ({self.title})"

    class Meta:
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')


class BitPinCurrency(BaseModelWithDate):
    bitasia_active = models.BooleanField(_("Bitasia Active"), default=True)
    active = models.BooleanField(_("BitPin Active"), default=True)
    title = models.CharField(_("Title (English)"), max_length=255)
    title_fa = models.CharField(_("Title (فارسی)"), max_length=255, blank=True)
    code = models.CharField(_("Code"), max_length=10)
    image = models.URLField(_("Image URL"), null=True, blank=True)
    min_withdraw = models.FloatField(_("Minimum Withdrawal"), blank=True,
                                     null=True)
    color = models.CharField(_("Color"), max_length=6)
    alias = models.CharField(_("Alias"), max_length=255, blank=True)
    withdraw_commission = models.FloatField(_("Withdrawal Commission"), blank=True,
                                            null=True)
    withdraw_commission_type = models.CharField(_("Withdrawal Commission Type"), max_length=10, blank=True, null=True)
    max_withdraw_commission = models.FloatField(_("Maximum Withdrawal Commission"),
                                                blank=True, null=True)
    tradable = models.BooleanField(_("Tradable"), default=False)
    for_test = models.BooleanField(_("For Test"), default=False)
    decimal = models.IntegerField(_("Decimal Places"), default=0)
    decimal_amount = models.IntegerField(_("Decimal Amount"), default=0)
    decimal_irt = models.IntegerField(_("Decimal (IRT)"))
    high_risk = models.BooleanField(_("High Risk"), default=False)
    show_high_risk = models.BooleanField(_("Show High Risk"), default=False)
    recommend_for_deposit_weight = models.IntegerField(_("Recommend for Deposit Weight"))
    for_loan = models.BooleanField(_("For Loan"), default=False)
    for_stake = models.BooleanField(_("For Stake"), default=False)
    network_ids = models.ManyToManyField(BitPinNetwork, blank=True)
    price_info_price = models.FloatField(_("Price"), null=True, blank=True)
    price_info_time = models.DateTimeField(_("Time"), null=True, blank=True)
    price_info_change = models.FloatField(_("Change"), null=True, blank=True)
    price_info_min = models.FloatField(_("Minimum"), null=True, blank=True)
    price_info_max = models.FloatField(_("Maximum"), null=True, blank=True)
    price_info_mean = models.FloatField(_("Mean"), null=True, blank=True)
    price_info_value = models.FloatField(_("Market Value"),
                                         null=True,
                                         blank=True)  # Assuming value refers to market value
    price_info_amount = models.FloatField(_("Market Amount"), null=True, blank=True)
    price_info_market_value = models.FloatField(_("Total Market Value"),
                                                null=True, blank=True)
    price_info_market_amount = models.FloatField(_("Total Market Amount"),
                                                 null=True, blank=True)
    price_info_usdt_price = models.FloatField(_("Price USDT"), null=True, blank=True)
    price_info_usdt_time = models.DateTimeField(_("Time USDT"), null=True, blank=True)
    price_info_usdt_change = models.FloatField(_("Change USDT"), null=True,
                                               blank=True)
    price_info_usdt_min = models.FloatField(_("Minimum USDT"), null=True, blank=True)
    price_info_usdt_max = models.FloatField(_("Maximum USDT"), null=True, blank=True)
    price_info_usdt_mean = models.FloatField(_("Mean USDT"), null=True, blank=True)
    price_info_usdt_value = models.FloatField(_("Market Value USDT"),

                                              null=True, blank=True)  # Assuming value refers to market value
    price_info_usdt_amount = models.FloatField(_("Market Amount USDT"),
                                               null=True, blank=True)
    price_info_usdt_market_value = models.FloatField(_("Total Market Value USDT"),
                                                     null=True, blank=True)
    price_info_usdt_market_amount = models.FloatField(_("Total Market Amount USDT"),
                                                      null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.title_fa})"

    class Meta:
        ordering = ("id",)
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
