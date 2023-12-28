from django.contrib import admin
from .models import OTP


# Register your models here.
@admin.register(OTP)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["code", "user_id", "created_at", "updated_at" ]