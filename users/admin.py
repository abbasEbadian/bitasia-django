from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CurrencyAdmin(TrackerAdmin):
    list_display = ("uid", "first_name", 'username')
