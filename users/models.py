# Create your models here.
import string
import uuid
from random import choice

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from authentication.utils import send_otp_sms
from exchange.models import BaseModelWithDate

auth_status = [
    ('unauthorized', 'احراز نشده'),
    ('level1', 'سطح یک'),
    ('level2', 'سطح دو'),
    ('level3', 'سطح سه'),
    ('pending', 'در حال بررسی مدارک'),
]


def get_file_path_for_birth(instance, filename):
    ext = filename.split('.')[-1]
    return "images/users/%d/birth_card.%s" % (instance.id, ext)


def get_file_path_for_national(instance, filename):
    ext = filename.split('.')[-1]
    return "images/users/%d/national_card.%s" % (instance.id, ext)


def get_file_path_for_avatar(instance, filename):
    return filename


def _generate_referral_code():
    characters = (string.digits + string.ascii_uppercase + string.ascii_lowercase).replace("l", "").replace("I",
                                                                                                            "").replace(
        "o", "").replace("O", "").replace("0", "")
    code = ''.join(choice(characters) for _ in range(7))
    return code


class CustomUser(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="شناسه", )
    mobile = models.CharField(max_length=11, verbose_name="شماره همراه")
    authentication_status = models.CharField(
        max_length=20, choices=auth_status, verbose_name="وضعیت احراز هویت", default="unauthorized")
    national_code = models.CharField(
        max_length=10, verbose_name="کد ملی", null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name="جنسیت", choices=[
        ("male", 'آقا'), ('female', 'خانم')], null=True, blank=True)
    birthdate = models.CharField(
        null=True, blank=True, verbose_name="تاریخ تولد")
    national_card_image = models.ImageField(
        verbose_name='تصویر کارت ملی', upload_to=get_file_path_for_national, null=True, blank=True, )
    birth_card_image = models.ImageField(
        verbose_name='تصویر شناسنامه', upload_to=get_file_path_for_birth, null=True, blank=True, )

    last_login = models.DateTimeField(verbose_name="آخرین ورود", null=True, blank=True, auto_now=True)
    authority_option_ids = models.ManyToManyField('authority.authorityruleoption')
    mobile_matched_national_code = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=8, default=_generate_referral_code)
    parent = models.ForeignKey("customuser", related_name="subsets", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.first_name and (self.first_name + " " + self.last_name + "(" + self.username + ")") or self.username

    class Meta:
        ordering = ("-id",)
        app_label = "users"
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_referral_incomes(self):
        return []

    @property
    def has_national_card_image(self):
        return bool(self.national_card_image)

    @property
    def has_birth_card_image(self):
        return bool(self.birth_card_image)

    def send_otp(self, otp_type):
        code, success = send_otp_sms(self.mobile, otp_type)
        if success:
            return self.otp_set.create(code=code, type=otp_type)
        return False

    def create_wallet(self, code):
        Currency = apps.get_model('bitpin', 'BitPinCurrency')
        try:
            currency = Currency.objects.get(code=code)
            wallet = self.wallets.create(currency_id=currency)
            return wallet
        except Exception as _:
            return None

    def get_wallet(self, code):
        wallet = self.wallets.filter(currency_id__code=code).first()
        if not wallet:
            wallet = self.create_wallet(code)

        return wallet

    def has_wallet(self, code):
        return self.wallets.filter(currency_id__code=code).exists()

    def log_login(self, successful, ip, reason=None):
        return self.loginhistory_set.create(successful=successful, ip=ip, reason=reason)


class LoginHistoryQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user_id=user)

    def objects(self):
        return self.all()


class LoginHistory(BaseModelWithDate):
    class Reason(models.TextChoices):
        INVALID_OTP = "invalid_otp", _("Invalid OTP")
        INVALID_PASSWORD = "invalid_password", _("Invalid Password")

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    successful = models.BooleanField(default=False)
    ip = models.CharField(default="0.0.0.0", max_length=15)
    reason = models.CharField(max_length=16, choices=Reason.choices, null=True, blank=True)

    class Meta:
        verbose_name = _("Login history")
        verbose_name_plural = _("Login histories")
