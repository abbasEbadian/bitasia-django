from django.contrib import admin

from .models import RialDeposit, VerifyLine, RialWithdraw


@admin.display(description="amount")
def sep_amount(obj):
    return f"{obj.amount:,}"


# Register your models here.
@admin.register(RialDeposit)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["factor_number", "user_id", sep_amount, "card_number", "status"]


@admin.register(RialWithdraw)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["factor_number", "user_id", sep_amount, "sheba_number", "status"]


@admin.register(VerifyLine)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["deposit_id", "ref_id", "message", "status", "result"]
