from django.db import models


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
