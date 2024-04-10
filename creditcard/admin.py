from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

from .models import CreditCard


@admin.register(CreditCard)
class ModelNameAdmin(TrackerAdmin):
    list_display = ('card_number', 'iban', "user_id", "approved")
