from django.contrib import admin

from .models import BitPinCurrency, BitPinNetwork, BitPinWalletAddress


class BitPinNetworkInline(admin.StackedInline):
    model = BitPinNetwork


@admin.register(BitPinCurrency)
class BitPinCurrencyAdmin(admin.ModelAdmin):
    filter_horizontal = ["network_ids"]
    list_display = (
        "id", "title", "title_fa", "code", "markup_percent", "price", "price_usdt", "get_networks")
    search_fields = ["title", "title_fa", "code"]

    @admin.display(description="networks")
    def get_networks(self, obj):
        return ",".join(map(lambda x: x.code, obj.network_ids.only("code").all()))


@admin.register(BitPinNetwork)
class BitPinNetworkAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "title", "title_fa")
    search_fields = ("code", "title", "title_fa")


@admin.register(BitPinWalletAddress)
class BitPinWalletAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "currency_id", "network_id", "address")
    search_fields = ["currency_id__title", "currency_id__title_fa", "currency_id__code"]
