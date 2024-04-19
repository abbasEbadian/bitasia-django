import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from bitpin.models import BitPinCurrency, BitPinNetwork
from exchange.models import BaseModelWithDate

User = get_user_model()


class Transaction(BaseModelWithDate):
    class Type(models.TextChoices):
        DEPOSIT = 'deposit', _("Deposit")
        WITHDRAW = 'withdraw', _("Withdraw")

    class Status(models.TextChoices):
        PENDING = 'pending', _("Pending")
        APPROVE = 'approve', _("Approve")
        CANCEL = 'cancel', _("Cancel")
        REJECT = 'reject', _("Reject")

    type = models.CharField(verbose_name=_("Transaction Type"), max_length=8, choices=Type.choices)
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=20, decimal_places=9)
    wallet_address = models.CharField(verbose_name=_("Wallet Address"), max_length=255)
    currency_id = models.ForeignKey(BitPinCurrency, verbose_name=_("Currency"), on_delete=models.RESTRICT)
    currency_current_value = models.PositiveBigIntegerField(
        verbose_name=_("The irt price at the time of placing the ordering."),
        default=0)
    network_id = models.ForeignKey(BitPinNetwork, verbose_name=_("Network"), on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    tx_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"))
    submit_date = models.DateTimeField(verbose_name=_("Submit Date"), blank=True, null=True)
    factor_number = models.CharField(max_length=255, verbose_name=_("Factor Number"))
    amount_after_commission = models.DecimalField(verbose_name=_("Amount after commission"), max_digits=20,
                                                  decimal_places=8, null=True, blank=True)
    applied_commission_amount = models.DecimalField(verbose_name=_("Commission in request time"), max_digits=20,
                                                    decimal_places=8, null=True, blank=True)

    def __str__(self):
        return f"{self.type} / {self.amount} {self.currency_id.code} / {self.user_id.username}"

    class Meta:
        ordering = ('-submit_date', '-create_date',)
        verbose_name = _("Crypto Transaction")
        verbose_name_plural = _("Crypto Transactions")

    def change_state(self, status):
        self.status = status
        self.save()

    def rollback_wallet(self):
        wallet = self.user_id.get_wallet(self.currency_id.code)
        wallet.charge(self.amount)
        wallet.save()
        return True

    def after_create_request(self):
        wallet = self.user_id.get_wallet(self.currency_id.code)
        amount_after_commission = self.currency_id.calculate_amount_after_withdraw_commission(self.amount,
                                                                                              self.network_id)
        self.amount_after_commission = amount_after_commission
        self.applied_commission_amount = self.currency_id.calculate_withdraw_commission(self.amount, self.network_id)
        wallet.charge(-1 * self.amount)
        wallet.save()
        return True

    def reject(self):
        self.rollback_wallet()
        self.submit_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.change_state(self.Status.REJECT)
        return True

    def cancel(self):
        self.rollback_wallet()
        self.submit_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.change_state(self.Status.CANCEL)
        return True

    def approve(self):
        self.submit_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.change_state(self.Status.APPROVE)
        return True


class Order(BaseModelWithDate):
    class Type(models.TextChoices):
        BUY = 'buy', _("Buy")
        SELL = 'sell', _("Sell")

    class Status(models.TextChoices):
        PENDING = 'pending', _("Pending")
        APPROVE = 'approve', _("Approve")
        CANCEL = 'cancel', _("Cancel")
        REJECT = 'reject', _("REJECT")

    type = models.CharField(verbose_name=_("Transaction Type"), max_length=8, choices=Type.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.RESTRICT)
    base_currency_id = models.ForeignKey(BitPinCurrency, related_name="usdt_order_set", on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=20, decimal_places=9, verbose_name=_("Amount"))
    submit_date = models.DateTimeField(verbose_name=_("Submit Date"), blank=True, null=True)
    currency_current_value = models.PositiveBigIntegerField(
        verbose_name=_("The irt price at the time of placing the order."),
        default=0)
    currency_currency_usdt_value = models.DecimalField(max_digits=20, decimal_places=9,
                                                       verbose_name=_("USDT price at the time of placing the order."),
                                                       default=0)
    factor_number = models.CharField(max_length=255, verbose_name=_("Factor Number"))

    def __str__(self):
        type = "Buy" if self.type == self.Type.BUY else "Sell"
        return f"{type} / {self.amount} {self.currency_id.code} / {self.user_id.username}"

    class Meta:
        ordering = ('-submit_date', '-create_date',)
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def change_state(self, status):
        self.status = status
        self.save()

    def get_wallet_code_for_decrease(self):
        if self.type == self.Type.SELL:
            return self.currency_id.code
        return self.base_currency_id.code

    def get_wallet_code_for_increase(self):
        if self.type == self.Type.SELL:
            return self.base_currency_id.code
        return self.currency_id.code

    def get_amount_for_decrease(self):
        if self.type == self.Type.SELL:
            return self.amount
        return self.amount * self.currency_id.get_price(self.base_currency_id.code)

    @staticmethod
    def get_amount_for_increase(type, amount, currency, base_currency_code="IRT"):
        if type == Order.Type.SELL:
            return amount * currency.get_price(base_currency_code)
        return amount

    def _get_amount_for_increase(self):
        return self.get_amount_for_increase(self.type, self.amount, self.currency_id, self.base_currency_id.code)

    @staticmethod
    def get_commission_amount(currency, _type, amount, base_currency_code="IRT"):
        comm = currency.buy_sell_commission
        comm_type = currency.buy_sell_commission_type
        if _type == Order.Type.SELL:
            comm_amount = comm * currency.get_price(base_currency_code)
            if comm_type == currency.CommissionType.PERCENT:
                comm_amount *= amount
            return comm_amount
        if comm_type == currency.CommissionType.VALUE:
            return comm
        return comm * amount

    def _get_commission_amount(self):
        return self.get_commission_amount(self.currency_id, self.type, self.amount, self.base_currency_id.code)

    def get_amount_after_commission(self):
        amount = self._get_amount_for_increase()
        commission_amount = self._get_commission_amount()
        return amount - commission_amount

    def after_create_request(self):
        wallet = self.user_id.get_wallet(self.get_wallet_code_for_decrease())
        wallet.charge(-1 * self.get_amount_for_decrease())
        wallet.save()
        return True

    def approve(self):
        wallet = self.user_id.get_wallet(self.get_wallet_code_for_increase())
        wallet.charge(self.get_amount_after_commission())
        self.submit_date = datetime.datetime.now(tz=datetime.timezone.utc)
        self.change_state(self.Status.APPROVE)
        return True


class Transfer(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=20, decimal_places=9, verbose_name=_("Amount"))
    successful = models.BooleanField()
    destination_mobile = models.CharField(max_length=11)

    class Meta:
        ordering = ('-create_date',)
        verbose_name = _("Transfer")
        verbose_name_plural = _("Transfers")


@receiver(post_save, sender=Transaction, dispatch_uid="update_transaction")
def update_transaction_factor(sender, instance, created, **kwargs):
    if created and not instance.factor_number and instance.pk:
        # CR : Crypto deposit
        # CW : Crypto withdraw
        prefix = instance.type == Transaction.Type.WITHDRAW and "CW" or "CD"
        instance.factor_number = f"{prefix}-{str(instance.pk).rjust(6, '0')}"
        instance.save()


@receiver(post_save, sender=Order, dispatch_uid="update_transaction")
def update_order_factor(sender, instance, created, **kwargs):
    if created and not instance.factor_number and instance.pk:
        # BO : Buy Order
        # CO : Sell Order
        prefix = instance.type == Order.Type.BUY and "BO" or "CO"
        instance.factor_number = f"{prefix}-{str(instance.pk).rjust(6, '0')}"
        instance.save()


post_save.connect(update_transaction_factor, sender=Transaction)
post_save.connect(update_order_factor, sender=Transaction)
