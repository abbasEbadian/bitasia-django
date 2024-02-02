from django.contrib import admin

from .models import RialDeposit


# Register your models here.
@admin.register(RialDeposit)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["factor_number", "user_id", "amount", "card_number", "status"]
