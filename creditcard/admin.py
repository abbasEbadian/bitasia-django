from django.contrib import admin

from .models import CreditCard


@admin.register(CreditCard)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'card_number', 'iban', "user_id", "approved")
