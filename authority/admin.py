from django.contrib import admin
from django.utils.translation import gettext as _

from .models import AuthorityRuleOption, AuthorityRule, AuthorityLevel, AuthorityRequest


@admin.register(AuthorityRule)
class AuthorityRuleAdmin(admin.ModelAdmin):
    list_display = ('title', "options")

    @admin.display(description=_("Options"))
    def options(self, obj):
        decade = [x.title for x in obj.option_ids.all()]
        return ", ".join(decade)


@admin.register(AuthorityRuleOption)
class AuthorityRuleOptionAdmin(admin.ModelAdmin):
    list_display = ('title', "field_key", "field_type", "type", "process_time", "min_value", "max_value", "is_form")


@admin.register(AuthorityLevel)
class AuthorityLevelAdmin(admin.ModelAdmin):
    list_display = ('level', "rules", "deposit_ir_limit", "deposit_ir_limit_text",
                    "withdraw_ir_limit", "withdraw_ir_limit_text",
                    "deposit_crypto_limit", "deposit_crypto_limit_text",
                    "withdraw_crypto_limit", "withdraw_crypto_limit_text")

    @admin.display(description=_("Rules"))
    def rules(self, obj):
        decade = [x.title for x in obj.rule_ids.all()]
        return ", ".join(decade)


@admin.register(AuthorityRequest)
class AuthorityRequestAdmin(admin.ModelAdmin):
    list_display = ('user_id', "rule_id", "approved", "admin_message")
