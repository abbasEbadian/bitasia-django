from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import gettext as _

from . import vars

User = get_user_model()

OtpTypes = [
    (vars.OTP_TYPE_LOGIN, _("Login")),
    (vars.OTP_TYPE_REGISTER, _("Register")),
    (vars.OTP_TYPE_RESET_PASSWORD, _("Reset Password")),
    (vars.OTP_TYPE_TRANSACTION, _("Make a Transaction"))
]


class OTP(models.Model):
    code = models.IntegerField(verbose_name='کد ارسالی', blank=False)
    user_id = models.ForeignKey(User, verbose_name='کاربر درخواست کننده', on_delete=SET_NULL, null=True)
    type = models.CharField(max_length=20, verbose_name='نوع کدتایید', default=vars.OTP_TYPE_LOGIN, choices=OtpTypes)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    def __str__(self):
        return f"{self.code}({self.type})"
