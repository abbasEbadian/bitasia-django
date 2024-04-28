from decimal import Decimal

from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.forms import forms
from django.utils.translation import gettext as _

from api.models import RoundedDecimalField
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
    class CommissionType(models.TextChoices):
        VALUE = 'value', _('Value')
        PERCENT = 'percent', _('Percent')

    show_in_dashboard = models.BooleanField(default=False)
    bitasia_active = models.BooleanField(_("Bitasia Active"), default=True)
    active = models.BooleanField(_("BitPin Active"), default=True)
    title = models.CharField(_("Title (English)"), max_length=255)
    title_fa = models.CharField(_("Title (فارسی)"), max_length=255, blank=True)
    code = models.CharField(_("Code"), max_length=10)
    image = models.URLField(_("Image URL"), null=True, blank=True)
    min_withdraw = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Minimum Withdrawal"),
                                       blank=True,
                                       null=True)
    color = models.CharField(_("Color"), max_length=6)
    alias = models.CharField(_("Alias"), max_length=255, blank=True)
    withdraw_commission = RoundedDecimalField(max_digits=18, decimal_places=5,
                                              verbose_name=_("Withdrawal Commission"),
                                              blank=True,
                                              null=True)
    withdraw_commission_type = models.CharField(_("Withdrawal Commission Type"), max_length=10, blank=True, null=True)
    max_withdraw_commission = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                  verbose_name=_("Maximum Withdrawal Commission"),
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
    price_info_price = models.PositiveBigIntegerField(verbose_name=_("Price"), default=0)
    price_info_time = models.DateTimeField(_("Time"), null=True, blank=True)
    price_info_change = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Change"),
                                            default=0.0)
    price_info_min = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Minimum"), default=0.0)
    price_info_max = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Maximum"), default=0.0)
    price_info_mean = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Mean"), default=0.0)
    price_info_value = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Market Value"),
                                           default=0.0)  # Assuming value refers to market value
    price_info_amount = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Market Amount"),
                                            default=0.0)
    price_info_market_value = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                  verbose_name=_("Total Market Value"),
                                                  default=0.0)
    price_info_market_amount = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                   verbose_name=_("Total Market Amount"),
                                                   default=0.0)
    price_info_usdt_price = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Price USDT"),
                                                default=0.0)
    price_info_usdt_time = models.DateTimeField(_("Time USDT"), null=True, blank=True)
    price_info_usdt_change = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Change USDT"),
                                                 default=0.0)
    price_info_usdt_min = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Minimum USDT"),
                                              default=0.0)
    price_info_usdt_max = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Maximum USDT"),
                                              default=0.0)
    price_info_usdt_mean = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Mean USDT"),
                                               default=0.0)
    price_info_usdt_value = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                verbose_name=_("Market Value USDT"),
                                                default=0.0)  # Assuming value refers to market value
    price_info_usdt_amount = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                 verbose_name=_("Market Amount USDT"),
                                                 default=0.0)
    price_info_usdt_market_value = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                       verbose_name=_("Total Market Value USDT"), default=0.0)
    price_info_usdt_market_amount = RoundedDecimalField(max_digits=18, decimal_places=5,
                                                        verbose_name=_("Total Market Amount USDT"), default=0.0)

    price = models.PositiveBigIntegerField(verbose_name=_("Sales Price"), default=0)
    price_usdt = RoundedDecimalField(max_digits=18, decimal_places=5, verbose_name=_("Sales USDT Price"),
                                     default=0)
    markup_percent = RoundedDecimalField(max_digits=5, decimal_places=5, verbose_name=_("Sales Markup Percent"),
                                         default=0.001)
    buy_sell_commission = RoundedDecimalField(max_digits=5, decimal_places=5,
                                              verbose_name=_("Buy Sell Commission"),
                                              default=0.001)
    buy_sell_commission_type = models.CharField(_("Buy Sell Commission Type"), max_length=10,
                                                choices=CommissionType.choices, default=CommissionType.PERCENT)

    def __str__(self):
        return f"{self.title} ({self.title_fa})"

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        BitPinCurrency.objects.filter(pk=instance.pk).update(price=instance.get_price(),
                                                             price_usdt=instance.get_price("USDT"))

    def get_price(self, currency_code="IRT"):
        new_irt_price = self.price_info_price * (1 + self.markup_percent)
        if currency_code != "IRT":
            return new_irt_price * self.price_info_usdt_price / self.price_info_price
        return new_irt_price

    def _has_network(self, network):
        return self.network_ids.all().contains(network)

    def get_withdraw_commission_obj(self, network):
        return self.withdrawcommission_set.filter(network_id=network.id).first()

    def _get_bitpin_commission(self, amount):
        withdraw_commission_klass = apps.get_model('commission', 'WithdrawCommission')
        if self.withdraw_commission_type == withdraw_commission_klass.CommissionType.VALUE:
            return self.withdraw_commission
        return amount * self.withdraw_commission

    def _get_bitasia_commission(self, amount, network):
        withdraw_commission_klass = apps.get_model('commission', 'WithdrawCommission')
        comm = self.get_withdraw_commission_obj(network)
        if comm.type == withdraw_commission_klass.CommissionType.VALUE:
            return Decimal(comm.amount)
        return Decimal(amount * comm.amount)

    def calculate_amount_after_commission(self, amount, network):
        c1 = self._get_bitpin_commission(amount)
        c2 = self._get_bitasia_commission(amount, network)
        return amount - (c1 + c2)

    def calculate_withdraw_commission(self, amount, network):
        return self._get_bitasia_commission(amount, network)

    def calculate_amount_after_withdraw_commission(self, amount, network):
        return amount - self.calculate_withdraw_commission(amount, network)

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
