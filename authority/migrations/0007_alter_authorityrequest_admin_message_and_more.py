# Generated by Django 4.2.11 on 2024-04-09 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0006_alter_authorityrequest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorityrequest',
            name='admin_message',
            field=models.CharField(blank=True, null=True, verbose_name='پیام مدیر'),
        ),
        migrations.AlterField(
            model_name='authorityruleoption',
            name='process_time',
            field=models.CharField(blank=True, help_text='۱روز ،\u200c ۲ساعت ...', verbose_name='زمان تقریبی بررسی'),
        ),
    ]