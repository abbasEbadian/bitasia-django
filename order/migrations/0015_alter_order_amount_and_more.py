# Generated by Django 4.2.11 on 2024-04-27 14:33

import api.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_order_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=api.models.RoundedDecimalField(decimal_places=5, max_digits=18, verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency_currency_usdt_value',
            field=api.models.RoundedDecimalField(decimal_places=5, default=0, max_digits=18, verbose_name='USDT price at the time of placing the order.'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=api.models.RoundedDecimalField(decimal_places=5, max_digits=18, verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount_after_commission',
            field=api.models.RoundedDecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='Amount after commission'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='applied_commission_amount',
            field=api.models.RoundedDecimalField(blank=True, decimal_places=5, max_digits=18, null=True, verbose_name='Commission in request time'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='amount',
            field=api.models.RoundedDecimalField(decimal_places=5, max_digits=18, verbose_name='مقدار'),
        ),
    ]
