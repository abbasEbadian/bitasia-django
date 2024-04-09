from django.contrib import admin

from commission.models import WithdrawCommission


@admin.register(WithdrawCommission)
class WithdrawCommissionAdmin(admin.ModelAdmin):
    list_display = ["id", "currency_id", "network_id", "amount", "type"]
