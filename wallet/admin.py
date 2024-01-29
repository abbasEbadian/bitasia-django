from django.contrib import admin

from wallet.models import Wallet, Currency


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance', 'user_id', 'currency_id')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol')
