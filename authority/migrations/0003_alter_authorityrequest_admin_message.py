# Generated by Django 4.2.8 on 2024-01-22 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0002_alter_authorityrequest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorityrequest',
            name='admin_message',
            field=models.CharField(blank=True, null=True, verbose_name='Admin message'),
        ),
    ]
