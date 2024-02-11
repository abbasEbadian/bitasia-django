from django.contrib import admin

from .models import RialDeposit, VerifyLine


# Register your models here.
@admin.register(RialDeposit)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["factor_number", "user_id", "amount", "card_number", "status"]


@admin.register(VerifyLine)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["deposit_id", "ref_id", "message", "status", "result"]
