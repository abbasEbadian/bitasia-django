# Generated by Django 4.2.11 on 2024-04-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_alter_wallet_options_alter_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=8, default=0.0, max_digits=20, verbose_name='موجودی'),
        ),
    ]
