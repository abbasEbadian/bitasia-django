from django.contrib import admin

from .models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress


class BitPinNetworkInline(admin.StackedInline):
    model = BitPinNetwork


@admin.register(BitPinCurrency)
class BitPinCurrencyAdmin(admin.ModelAdmin):
    filter_horizontal = ["network_ids"]


list_display = (
    "id", "title", "title_fa", "code", "price_info_price", "markup_percent", "price", "price_info_usdt_price")
search_fields = ["title", "title_fa", "code"]


@admin.register(BitPinNetwork)
class BitPinNetworkAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "title", "title_fa")


@admin.register(BitPinWalletAddress)
class BitPinWalletAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "currency_id", "network_id", "address")
