import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

import environ
import requests
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from authentication.exception import CustomError
from authority.models import BaseModelWithDate
from exchange.error_codes import ERRORS

_logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

json_headers = {
    'content-type': 'application/json',
    'accept': 'application/json',
}

User = get_user_model()


@dataclass
class RialDepositVars:
    create_url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    verify_url = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    merchant_id = env('ZARINPAL_MERCHANT_ID')
    callback_url = env('CALLBACK_URL')


class RialDeposit(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(_("Amount"), decimal_places=0, max_digits=6)
    factor_number = models.CharField(_("Factor number"), unique=True)
    gateway_token = models.CharField(_("Gateway Token"), blank=True, null=True, help_text='Authority')
    gateway_status = models.CharField(_("Gateway Status"), blank=True, null=True)
    gateway_fee = models.DecimalField(_("Gateway Fee"), blank=True, decimal_places=0, max_digits=5, null=True)
    gateway_fee_type = models.CharField(_("Gateway Fee Type"), blank=True, null=True)
    gateway_message = models.CharField(_("Gateway Message"), blank=True, null=True)

    card_number = models.CharField(_("Card Number"), max_length=16)
    status = models.CharField(_("Status"), choices=[
        ('pending', _("Pending")),
        ('success', _("Success")),
        ('cancel', _("Cancel")),
    ], default="pending")

    def __str__(self):
        return f"{_('Rial deposit')} | {self.amount}"

    def get_user_metadata(self):
        return {
            "order_id": self.factor_number,
            "mobile": self.user_id.mobile,
            "email": self.user_id.email or 'abbasebadiann@gmail.com',
            "card_pan": self.card_number
        }

    class Meta:
        verbose_name = _("Rial deposit")
        verbose_name_plural = _("Rial deposits")

    def cancel(self):
        self.status = 'cancel'
        self.save()

    def is_pending(self):
        return self.status == 'pending'

    def success(self):
        wallet = self.user_id.get_wallet("IRT")
        self.status = 'success'
        charged = wallet.charge(self.amount)
        self.save()
        return charged

    def create_payment(self):
        body = {
            "merchant_id": RialDepositVars.merchant_id,
            "callback_url": RialDepositVars.callback_url,
            "amount": self.amount,
            "currency": "IRT",
            "metadata": self.get_user_metadata(),
            "description": f" واریز {self.amount} تومان برای شارژ کیف پول ریالی بیت آسیا",
        }

        req = requests.post(RialDepositVars.create_url, data=json.dumps(body), headers=json_headers)
        if not req or str(req.status_code) != '200':
            raise CustomError(ERRORS.ERROR_GATEWAY)

        r = req.json().get("data", {})

        if str(req.status_code)[0] == '2':
            token = r.get('authority', "")

            status = r.get('code')
            if str(status) != '100':
                raise CustomError(ERRORS.custom_message_error(r.get("message")))

            self.gateway_token = token
            self.gateway_status = status
            self.gateway_fee_type = r.get('fee_type', "")
            self.gateway_fee = r.get('fee', "")
            self.gateway_message = r.get('gateway_message')
            self.save()
        else:
            err = r.get('errors')
            err = err[0] if isinstance(err, list) else err
            raise CustomError(ERRORS.custom_message_error(str(err)))
        return f"https://www.zarinpal.com/pg/StartPay/{self.gateway_token}"

    def check_transaction_integrity(self):
        body = {
            "merchant_id": RialDepositVars.merchant_id,
            "amount": int(self.amount),
            "authority": self.gateway_token
        }
        try:
            req = requests.post(RialDepositVars.verify_url, data=json.dumps(body), headers=json_headers)
            line = {}
            if req.status_code not in [200, 400]:
                line["status"] = req.status_code
                line["message"] = "Cant connect to Zarinpal"
                self.verifyline_set.create(**line)
                _logger.error("Zarinpal -> check_transaction_integrity: not %d " % req.status_code)
                raise CustomError(ERRORS.ERROR_GATEWAY)
            result = req.json()
            data = result.get("data", [])
            success = True
            if isinstance(data, list) and len(data) == 0:
                data = result.get("errors")
                success = False
            else:
                line["ref_id"] = data.get('ref_id')
                line["card_pan"] = data.get('card_pan')
                line["card_hash"] = data.get('card_hash')
                line["fee_type"] = data.get('fee_type')
                line["fee"] = data.get('fee')
                line["result"] = "ok"
            line["status"] = data.get('code')
            line["message"] = data.get('message')
            self.verifyline_set.create(**line)
            self.save()
            return success
        except Exception as e:
            print(e)
            return False


class VerifyLine(BaseModelWithDate):
    deposit_id = models.ForeignKey(RialDeposit, on_delete=models.CASCADE)
    ref_id = models.CharField(_("Verify Ref ID"), blank=True, null=True)
    message = models.CharField(_("Verify message"), blank=True, null=True)
    status = models.CharField(_("Verify status"), blank=True, null=True)
    result = models.CharField(_("Result"), default="nok", choices=[('ok', "OK"), ("nok", "NOK")])
    card_pan = models.CharField(_("Card"), blank=True, null=True)
    card_hash = models.CharField(_("Card Hash"), blank=True, null=True)
    fee_type = models.CharField(_("Fee Type"), blank=True, null=True)
    fee = models.FloatField(_("Fee"), blank=True, null=True)

    class Meta:
        verbose_name = _("Verify Deposit Attempt")
        verbose_name_plural = _("Verify Deposit Attempts")


@receiver(post_save, sender=RialDeposit, dispatch_uid="update_rial_deposit")
def update_rial_deposit(sender, instance, created, **kwargs):
    if created and not instance.factor_number and instance.pk:
        # RD : Rial Deposit
        instance.factor_number = f"RD-{str(instance.pk).rjust(4, '0')}"
        instance.save()


post_save.connect(update_rial_deposit, sender=RialDeposit)
