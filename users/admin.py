from django.contrib import admin

from .models import CustomUser, LoginHistory


@admin.register(CustomUser)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("uid", "first_name", 'username')


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user_id", "successful", "ip", "create_date")
