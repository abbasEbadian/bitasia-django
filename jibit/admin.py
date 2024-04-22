from django.contrib import admin

from jibit.models import JibitRequest


@admin.register(JibitRequest)
class JibitRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "type", "create_date", "matched", "result_json"]
    list_display_links = ["user_id"]
