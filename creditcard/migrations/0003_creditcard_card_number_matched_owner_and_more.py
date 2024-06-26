# Generated by Django 4.2.11 on 2024-04-22 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0002_alter_creditcard_options_alter_creditcard_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='card_number_matched_owner',
            field=models.BooleanField(default=False, verbose_name='Card number matched owner credit card'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='iban_matched_owner',
            field=models.BooleanField(default=False, verbose_name='Card number matched owner credit card'),
        ),
    ]
