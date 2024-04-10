from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

from wallet.models import Wallet


@admin.display(description="balance")
def sep_balance(obj):
    return f"{obj.balance:,}"


@admin.register(Wallet)
class WalletAdmin(TrackerAdmin):
    list_display = ('id', sep_balance, 'user_id', 'currency_id')
