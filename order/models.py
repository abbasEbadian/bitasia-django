from bitpin.models import BitPinCurrency, BitPinNetwork
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
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
        REJECT = 'reject', _("REJECT")

    type = models.CharField(verbose_name=_("Transaction Type"), max_length=8, choices=Type.choices)
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=20, decimal_places=8)
    wallet_address = models.CharField(verbose_name=_("Wallet Address"), max_length=255)
    currency_id = models.ForeignKey(BitPinCurrency, verbose_name=_("Currency"), on_delete=models.RESTRICT)
    network_id = models.ForeignKey(BitPinNetwork, verbose_name=_("Network"), on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.RESTRICT)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    tx_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"))
    submit_date = models.DateTimeField(verbose_name=_("Submit Date"), blank=True, null=True)

    def __str__(self):
        return f"{self.type} / {self.amount} {self.currency_id.code} / {self.user_id.username}"

    class Meta:
        ordering = ('-id',)
        verbose_name = _("Crypto Transaction")
        verbose_name_plural = _("Crypto Transactions")

    def change_state(self, status):
        self.status = status
        self.save()

# class Purchase(BaseModelWithDate):
#     user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
#     currency_id = models.ForeignKey(BitPinCurrency, on_delete=models.RESTRICT)
#
#     status = models.CharField(max_length=10, choices=[
#         (PENDING, PENDING_LABEL),
#         (CANCEL, CANCEL_LABEL),
#         (SUCCESS, SUCCESS_LABEL)
#     ])
#     amount = models.DecimalField(max_digits=20, decimal_places=8, verbose_name=_("Amount"))
#     track_id = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Track ID"))
#
#     def __str__(self):
#         return f"Purchase / {self.amount} {self.currency_id.code} / {self.user_id.username}"
#
#     class Meta:
#         ordering = ('-id',)
#         verbose_name = _("Purchase")
#         verbose_name_plural = _("Purchases")
#
#     def confirm(self):
#         irt_wallet = self.user_id.get_wallet("IRT")
#         if irt_wallet.balance < 10000:
#             return "fail", _("Not enough balance.")
#         irt_wallet.charge(-10000)
#         wallet = self.user_id.get_wallet(self.currency_id.code)
#         wallet.charge(self.amount)
#         return "success", _("Confirmed successfully")
