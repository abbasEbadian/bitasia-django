from django.contrib import admin

from .models import BitPinCurrency, BitPinNetwork


@admin.register(BitPinCurrency)
class BitPinCurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_fa", "code", "price_info_price", "price_info_usdt_price")
    search_fields = ["title", "title_fa", "code"]


@admin.register(BitPinNetwork)
class BitPinNetworkAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "title_fa")
