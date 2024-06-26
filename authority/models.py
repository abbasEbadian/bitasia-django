from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from exchange.models import BaseModel

User = get_user_model()


class AuthorityRuleOption(BaseModel):
    title = models.CharField(_("title"))
    field_key = models.CharField(_("field key"))
    field_type = models.CharField(_("field type"),
                                  choices=[("text", "text"), ("image", "image"), ("boolean", "boolean")])
    type = models.CharField(_("type"), choices=[('range', _("Range")), ('defined', _("Defined"))])
    is_form = models.BooleanField(_("Is form"), default=False)
    min_value = models.IntegerField(_("min value"), blank=True)
    max_value = models.IntegerField(_("max value"), blank=True)
    process_time = models.CharField(_("َApproximate processing time"), help_text=_("1 Day, 2 Hours, ..."), blank=True)

    class Meta:
        verbose_name = _("Authority rule option")
        verbose_name_plural = _("Authority rule options")

    def __str__(self):
        return f"{_('Authority rule option')} ({self.title})"


class AuthorityRule(BaseModel):
    title = models.CharField(_("title"))
    option_ids = models.ManyToManyField(AuthorityRuleOption)
    sequence = models.IntegerField(_("Priority"), default=1)

    class Meta:
        ordering = ('sequence',)
        verbose_name = _("Authority rule")
        verbose_name_plural = _("Authority rules")

    def __str__(self):
        return self.title


class AuthorityLevel(BaseModel):
    level = models.CharField(_("Level"))
    rule_ids = models.ManyToManyField(AuthorityRule)
    deposit_ir_limit = models.IntegerField(_("daily Rial deposit limit"))
    deposit_ir_limit_text = models.CharField(_("daily Rial deposit limit description"))
    withdraw_ir_limit = models.IntegerField(_("daily Rial withdraw limit"))
    withdraw_ir_limit_text = models.CharField(_("daily Rial withdraw limit description"))
    deposit_crypto_limit = models.IntegerField(_("daily Crypto deposit limit"))
    deposit_crypto_limit_text = models.CharField(_("daily Crypto deposit limit description"))
    withdraw_crypto_limit = models.IntegerField(_("daily Crypto withdraw limit"))
    withdraw_crypto_limit_text = models.CharField(_("daily Crypto withdraw limit description"))

    class Meta:
        ordering = ('level',)

    def __str__(self):
        return f"{_('Level')} {self.level}"


class AuthorityRequest(BaseModel):
    user_id = models.ForeignKey(User, verbose_name=_("Requesting user"), on_delete=models.CASCADE)
    rule_id = models.ForeignKey(AuthorityRule, verbose_name=_("Rule ID"), on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    admin_message = models.CharField(_("Admin message"), blank=True, null=True)

    def approve(self):
        self.approved = True
        self.save()

    class Meta:
        verbose_name = _("Authority request")
        verbose_name_plural = _("Authority requests")

    def __str__(self):
        return f"{_('Authority request')} - {str(self.user_id or '')}"


def get_user_level(user):
    level = 0
    user_approved_rules = [x.rule_id.id for x in user.authorityrequest_set.filter(approved=True)]
    for lvl in AuthorityLevel.objects.all():
        for rule in lvl.rule_ids.all():
            if rule.id not in user_approved_rules:
                return level
        level = lvl.level

    return level
