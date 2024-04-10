from ModelTracker.Tracker import TrackerAdmin
from django.contrib import admin

from .models import OTP


# Register your models here.
@admin.register(OTP)
class ModelNameAdmin(TrackerAdmin):
    list_display = ["code", "user_id", "created_at", "updated_at", "type"]
