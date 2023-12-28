from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import SET_NULL

User = get_user_model()


class OTP(models.Model):
    code = models.IntegerField(verbose_name='کد ارسالی', blank=False)
    user_id = models.ForeignKey(User, verbose_name='کاربر درخواست کننده', on_delete=SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')

    def __str__(self):
        return str(self.code)
