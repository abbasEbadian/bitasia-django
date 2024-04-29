# Generated by Django 4.2.11 on 2024-04-28 15:13

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpin', '0021_alter_bitpincurrency_buy_sell_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitpincurrency',
            name='buy_sell_commission',
            field=api.models.RoundedDecimalField(decimal_places=5, default=0.001, max_digits=5, verbose_name='Buy Sell Commission'),
        ),
        migrations.AlterField(
            model_name='bitpincurrency',
            name='markup_percent',
            field=api.models.RoundedDecimalField(decimal_places=5, default=0.001, max_digits=5, verbose_name='Sales Markup Percent'),
        ),
        migrations.AlterField(
            model_name='bitpincurrency',
            name='price',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Sales Price'),
        ),
        migrations.AlterField(
            model_name='bitpincurrency',
            name='price_info_price',
            field=models.PositiveBigIntegerField(default=0, verbose_name='قیمت تومانی'),
        ),
    ]