from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.forms import forms
from django.utils.translation import gettext as _

from exchange.models import BaseModelWithDate


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
    show_in_dashboard = models.BooleanField(default=False)
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

    price = models.FloatField(_("Sales Price"), default=0)
    markup_percent = models.FloatField(_("Sales Markup Percent"), default=0)

    def __str__(self):
        return f"{self.title} ({self.title_fa})"

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        BitPinCurrency.objects.filter(pk=instance.pk).update({"price": instance.get_price()})

    def get_price(self):
        return self.price_info_price + (self.price_info_price * self.markup_percent)

    def _has_network(self, network):
        return self.network_ids.all().contains(network)

    def _get_bitpin_commission(self, amount):
        WithdrawCommission = apps.get_model('commission', 'WithdrawCommission')

        if self.withdraw_commission_type == WithdrawCommission.CommissionType.VALUE:
            return self.withdraw_commission
        return amount * self.withdraw_commission

    def _get_bitasia_commission(self, amount, network):
        WithdrawCommission = apps.get_model('commission', 'WithdrawCommission')

        comm = self.withdrawcommission_set.filter(network_id=network.id).first()

        if comm.type == WithdrawCommission.CommissionType.VALUE:
            return comm.amount
        return amount * comm.amount

    def calculate_amount_after_commission(self, amount, network):
        c1 = self._get_bitpin_commission(amount)
        c2 = self._get_bitasia_commission(amount, network)
        print(f"karmozd: \n{c1=} \n{c2=}")
        return amount - (c1 + c2)

    class Meta:
        ordering = ("-show_in_dashboard", "-price_info_price")
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class BitPinWalletAddress(BaseModelWithDate):
    address = models.CharField(_("Address"), max_length=255)
    currency_id = models.ForeignKey(BitPinCurrency, verbose_name=_("Currency"), on_delete=models.CASCADE)
    network_id = models.ForeignKey(BitPinNetwork, verbose_name=_("Network"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address} / {self.currency_id.code} / {self.network_id.code}"

    def clean(self):
        if not self.currency_id._has_network(self.network_id):
            raise forms.ValidationError(_("Invalid network ID. Provided network must be present in currency networks."))
        if self._state.adding and BitPinWalletAddress.objects.filter(currency_id=self.currency_id,
                                                                     network_id=self.network_id).exists():
            raise forms.ValidationError(_("Already exists, Try to update."))
        return super().clean()

    class Meta:
        verbose_name = _('BitPin Wallet Address')
        verbose_name_plural = _('BitPin Wallet Addresses')


post_save.connect(BitPinCurrency.post_save, sender=BitPinCurrency)
