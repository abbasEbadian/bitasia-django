from django.contrib import admin

#
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "type", "user_id", "currency_id", "network_id", "amount", "status", "wallet_address", "tx_id", "submit_date")

# @admin.register(Purchase)
# class PurchaseAdmin(admin.ModelAdmin):
#     list_display = ("user_id", "currency_id", "amount", "status", "track_id")
