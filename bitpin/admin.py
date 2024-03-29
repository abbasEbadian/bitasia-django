from django.contrib import admin

from .models import BitPinCurrency, BitPinNetwork


@admin.register(BitPinCurrency)
class BitPinCurrencyAdmin(admin.ModelAdmin):
    list_display = ("title", "title_fa", "code", "price_info_price", "price_info_usdt_price")


@admin.register(BitPinNetwork)
class BitPinNetworkAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "title_fa")
