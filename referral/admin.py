from django.contrib import admin

from referral.models import ReferralProgram


@admin.register(ReferralProgram)
class ReferralProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'min_subset_count', 'max_subset_count', 'percent')
