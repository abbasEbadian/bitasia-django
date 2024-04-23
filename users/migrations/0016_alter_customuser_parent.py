# Generated by Django 4.2.11 on 2024-04-23 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_customuser_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subsets', to=settings.AUTH_USER_MODEL),
        ),
    ]
