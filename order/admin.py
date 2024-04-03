from django.contrib import admin

from .models import Order, Purchase


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user_id", "currency_id", "amount", "status")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user_id", "currency_id", "amount", "status", "track_id")
