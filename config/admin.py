from django.contrib import admin
from solo.admin import SingletonModelAdmin

from config.models import JibitConfiguration

admin.site.register(JibitConfiguration, SingletonModelAdmin)
