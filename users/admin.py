from django.contrib import admin
from .models import CustomUser
# Register your models here


@admin.register(CustomUser)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("uid", "first_name", 'username')
