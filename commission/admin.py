from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

from commission.models import WithdrawCommission


@admin.register(WithdrawCommission)
class WithdrawCommissionAdmin(TrackerAdmin):
    list_display = ["id", "currency_id", "network_id", "amount", "type"]
