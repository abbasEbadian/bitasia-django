from django.contrib import admin

from .models import OTP


# Register your models here.
@admin.register(OTP)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "user_id", "create_date", "write_date", "type", "consumed", "expired"]
