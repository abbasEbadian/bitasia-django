from django.contrib import admin
from django.utils.translation import gettext as _

from .models import AuthorityRuleOption, AuthorityRule


@admin.register(AuthorityRule)
class AuthorityRuleAdmin(admin.ModelAdmin):
    list_display = ('title', "options"
                    , "deposit_ir_limit", "deposit_ir_limit_text",
                    "withdraw_ir_limit", "withdraw_ir_limit_text",
                    "deposit_crypto_limit", "deposit_crypto_limit_text",
                    "withdraw_crypto_limit", "withdraw_crypto_limit_text")

    @admin.display(description=_("Options"))
    def options(self):
        decade = [x.title for x in self.option_ids]
        return ", ".join(decade)


@admin.register(AuthorityRuleOption)
class AuthorityRuleOptionAdmin(admin.ModelAdmin):
    list_display = ('title', "type", "process_time", "min_value", "max_value", "is_form")
