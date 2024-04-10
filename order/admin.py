from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

#
from .models import Transaction, Order


@admin.register(Transaction)
class TransactionAdmin(TrackerAdmin):
    list_display = ("id", "type", "user_id", "currency_id", "network_id", "amount", "status", "wallet_address",
                    "tx_id", "submit_date")


@admin.register(Order)
class OrderAdmin(TrackerAdmin):
    list_display = ("id", "type", "user_id", "currency_id", "amount", "status", "submit_date")
