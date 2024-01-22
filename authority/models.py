from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class BaseModelWithDate(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthorityRuleOption(BaseModelWithDate):
    title = models.CharField(_("title"))
    field_key = models.CharField(_("field key"))
    type = models.CharField(_("type"), choices=[('range', _("Range")), ('defined', _("Defined"))])
    is_form = models.BooleanField(_("Is form"), default=False)
    min_value = models.IntegerField(_("min value"))
    max_value = models.IntegerField(_("max value"))
    process_time = models.CharField(_("َApproximate processing time"), help_text=_("1 Day, 2 Hours, ..."))


class AuthorityRule(BaseModelWithDate):
    title = models.CharField(_("title"))
    option_ids = models.ManyToManyField(AuthorityRuleOption)

    deposit_ir_limit = models.IntegerField(_("daily Rial deposit limit"))
    deposit_ir_limit_text = models.CharField(_("daily Rial deposit limit description"))
    withdraw_ir_limit = models.IntegerField(_("daily Rial withdraw limit"))
    withdraw_ir_limit_text = models.CharField(_("daily Rial withdraw limit description"))
    deposit_crypto_limit = models.IntegerField(_("daily Crypto deposit limit"))
    deposit_crypto_limit_text = models.CharField(_("daily Crypto deposit limit description"))
    withdraw_crypto_limit = models.IntegerField(_("daily Crypto withdraw limit"))
    withdraw_crypto_limit_text = models.CharField(_("daily Crypto withdraw limit description"))


class AuthorityRequest(BaseModelWithDate):
    user_id = models.ForeignKey(User, verbose_name=_("Requesting user"), on_delete=models.CASCADE)
    AuthorityRule = models.ForeignKey(AuthorityRule, verbose_name=_("Rule ID"), on_delete=models.CASCADE)
    approved = models.BooleanField()
    admin_message = models.CharField(_("Admin message"))
