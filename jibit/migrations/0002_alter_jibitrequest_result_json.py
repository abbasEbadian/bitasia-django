# Generated by Django 4.2.11 on 2024-04-22 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jibit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jibitrequest',
            name='result_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]