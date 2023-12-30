# Create your models here.
import uuid

from authentication import vars
from authentication.utils import send_otp_sms
from django.contrib.auth.models import AbstractUser
from django.db import models

auth_status = [
    ('unauthorized', 'احراز نشده'),
    ('level1', 'سطح یک'),
    ('level2', 'سطح دو'),
    ('level3', 'سطح سه'),
    ('pending', 'در حال بررسی مدارک'),
]


def get_file_path_for_birth(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/national_cards/%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_file_path_for_national(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/birth_cards/%s.%s" % (uuid.uuid4(), ext)
    return filename


def get_file_path_for_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "images/avatars/%s.%s" % (uuid.uuid4(), ext)
    return filename


class CustomUser(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="شناسه")
    mobile = models.CharField(max_length=11, verbose_name="شماره همراه")
    authentication_status = models.CharField(
        max_length=20, choices=auth_status, verbose_name="وضعیت احراز هویت", default="unauthorized")
    national_code = models.CharField(
        max_length=10, verbose_name="کد ملی", null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name="جنسیت", choices=[
        ("male", 'آقا'), ('female', 'خانم')], null=True, blank=True)
    birth_date = models.DateTimeField(
        null=True, blank=True, verbose_name="تاریخ تولد")
    national_card_image = models.ImageField(
        verbose_name='تصویر کارت ملی', upload_to=get_file_path_for_birth, null=True, blank=True, )
    birth_card_image = models.ImageField(
        verbose_name='تصویر شناسنامه', upload_to=get_file_path_for_national, null=True, blank=True, )
    avatar_image = models.ImageField(
        verbose_name='تصویر کاربری', upload_to=get_file_path_for_avatar, null=True, blank=True, )
    last_login = models.DateTimeField(verbose_name="آخرین ورود", null=True, blank=True, auto_now=True)

    def __str__(self):
        return self.first_name and (self.first_name + " " + self.last_name + "(" + self.username + ")") or self.username

    class Meta:
        app_label = "users"
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"

    def save(self, *args, **kwargs):
        # if needed sth
        return super().save(*args, **kwargs)

    @property
    def has_national_card_image(self):
        return not not self.national_card_image

    @property
    def has_birth_card_image(self):
        return not not self.birth_card_image and True or False

    @property
    def has_avatar_image(self):
        return not not self.avatar_image and True or False

    def send_otp(self, type=vars.OTP_TYPE_LOGIN):
        code, success = send_otp_sms(self.mobile)
        if success:
            self.otp_set.create(code=code, type=type)
            return True
        return False

    def validate_otp(self, code, type=vars.OTP_TYPE_LOGIN):
        return not not self.otp_set.filter(code=code, type=type)
