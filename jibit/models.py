import requests
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from config.models import JibitConfiguration
from exchange.models import BaseModelWithDate

User = get_user_model()


class JibitRequest(BaseModelWithDate):
    class Type(models.TextChoices):
        NATIONAL_WITH_MOBILE = "national_with_mobile", _("Check national code with mobile number")
        NATIONAL_WITH_CARD = "national_with_creditcard", _("Check national code with credit card number")

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=24, choices=Type.choices)
    result_json = models.JSONField(null=True, blank=True)
    matched = models.BooleanField(default=False)
    successful_request = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id}: {self.type}"

    def _send_mobile_national_matching_test_request(self):
        url = "https://napi.jibit.ir/ide/v1/services/matching"
        jibit_conf = JibitConfiguration.get_solo()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {jibit_conf.token}"
        }
        data = {
            "mobileNumber": self.user_id.mobile,
            "nationalCode": self.user_id.national_code,
        }
        res = requests.get(url, headers=headers, params=data)
        status_code = res.status_code
        if status_code == 200:
            res = res.json()
            matched = "matched" in res and res["matched"] or False
            self.successful_request = True
            self.result_json = res
            self.matched = matched
            self.user_id.mobile_matched_national_code = matched
            self.user_id.save()
        elif status_code == 400:
            self.result_json = res
        elif str(res.status_code).startswith("5"):
            self.successful_request = False
            self.result_json = {"error": "Connection fail"}
        self.save()

    def _jibit_check_card_with_national_code(self, card_number=None, iban=""):
        url = "https://napi.jibit.ir/ide/v1/services/matching"
        birth_date = self.user_id.birthdate
        national_code = self.user_id.national_code
        if not iban and not card_number:
            return None
        birthDate = "".join([x for x in str(birth_date) if x.isdigit()])

        jibit_conf = JibitConfiguration.get_solo()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {jibit_conf.token}"
        }
        data = {
            "birthDate": birthDate,
            "nationalCode": national_code,
        }
        if iban:
            data["iban"] = iban
        elif card_number:
            data["cardNumber"] = card_number
        res = requests.get(url, headers=headers, params=data)
        status_code = res.status_code
        if status_code == 200:
            res = res.json()
            matched = "matched" in res and res["matched"] or False
            self.successful_request = True
            self.result_json = res
            self.matched = matched
            if card_number and matched:
                self.user_id.creditcard_set.filter(card_number=card_number).update(card_number_matched_owner=matched)
            if iban and matched:
                self.user_id.creditcard_set.filter(iban=iban).update(iban_matched_owner=matched)
            self.user_id.save()
        if status_code == 400:
            res = res.json()
            self.result_json = res

        elif str(status_code).startswith("5"):
            self.successful_request = False
            self.result_json = {"error": "Connection fail"}
        self.save()

    def send_request(self, card_number=None, iban=None):
        if self.type == self.Type.NATIONAL_WITH_MOBILE:
            self._send_mobile_national_matching_test_request()
        elif self.type == self.Type.NATIONAL_WITH_CARD:
            self._jibit_check_card_with_national_code(card_number, iban)

    class Meta:
        verbose_name = _("Jibit Reqeust")
        verbose_name_plural = _("Jibit Requests")
