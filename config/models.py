from django.db import models
from solo.models import SingletonModel


class JibitConfiguration(SingletonModel):
    token = models.CharField(max_length=255, unique=True, default="")
    refresh = models.CharField(max_length=255, unique=True, default="")
    last_call_success = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Jibit Configuration"

    class Meta:
        verbose_name = "Jibit Configuration"
