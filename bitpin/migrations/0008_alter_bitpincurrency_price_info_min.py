# Generated by Django 4.2.8 on 2024-04-03 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpin', '0007_alter_bitpincurrency_price_info_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitpincurrency',
            name='price_info_min',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True, verbose_name='Minimum'),
        ),
    ]
