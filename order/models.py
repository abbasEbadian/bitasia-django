import json
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

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

json_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

User = get_user_model()


@dataclass
class RialDepositVars:
    create_url = " https://ipg.vandar.io/api/v3/send/"
    api_key = env('VANDAR_API_KEY')
    api_token = env('VANDAR_TOKEN')
    callback_url = env('VANDAR_CALLBACK')


class RialDeposit(BaseModelWithDate):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(_("Amount"), decimal_places=0, max_digits=6)
    factor_number = models.CharField(_("Factor number"), unique=True)
    gateway_token = models.CharField(_("Gateway Token"), blank=True)
    gateway_status = models.CharField(_("Gateway Status"), blank=True)
    card_number = models.CharField(_("Card Number"), max_length=16)
    status = models.CharField(_("Status"), choices=[
        ('pending', _("Pending")),
        ('success', _("Success")),
        ('cancel', _("Cancel")),
    ], default="pending")

    def __str__(self):
        return f"{_('Rial deposit')} | {self.amount}"

    class Meta:
        verbose_name = _("Rial deposit")
        verbose_name_plural = _("Rial deposits")

    def get_headers(self):
        return {**json_headers, "Authorization": f"Bearer {RialDepositVars.api_token}"}

    def create_payment(self):
        headers = self.get_headers()
        try:
            body = {
                "api_key": RialDepositVars.api_key,
                "callback_url": RialDepositVars.callback_url,
                "amount": self.amount,
                "mobile_number": self.user_id and self.user_id.mobile,
                "factorNumber": self.factor_number,
                "description": f" واریز {self.amount} تومان برای شارژ کیف پول ریالی بیت آسیا",
                "valid_card_number": self.card_number
            }
            url = RialDepositVars.create_url

            req = requests.post(url, data=json.dumps(body), headers=headers)
            r = req.json()
            print(r)
            if str(req.status_code)[0] == '2':
                token = r.get('token')
                status = r.get('status')
                self.gateway_token = token
                self.gateway_status = status
                self.save()
                test = requests.get(f"https://ipg.vandar.io/v3/{self.gateway_token}")
                print(test.json())
            else:
                err = r.get('errors')
                err = err[0] if isinstance(err, list) else err
                raise CustomError(ERRORS.custom_message_error(str(err)))
            return f"https://ipg.vandar.io/v3/{self.gateway_token}"
        except Exception as e:
            print(e)
            raise CustomError(ERRORS.ERROR_GATEWAY)


@receiver(post_save, sender=RialDeposit, dispatch_uid="update_rial_deposit")
def update_rial_deposit(sender, instance, created, **kwargs):
    if created and not instance.factor_number and instance.pk:
        instance.factor_number = f"RD-{str(instance.pk).rjust(4, '0')}"
        instance.save()


post_save.connect(update_rial_deposit, sender=RialDeposit)
