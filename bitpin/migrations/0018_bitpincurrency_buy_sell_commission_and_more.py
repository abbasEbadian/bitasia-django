# Generated by Django 4.2.11 on 2024-04-19 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpin', '0017_alter_bitpincurrency_markup_percent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitpincurrency',
            name='buy_sell_commission',
            field=models.DecimalField(decimal_places=5, default=0.001, max_digits=10, verbose_name='Buy Sell Commission'),
        ),
        migrations.AddField(
            model_name='bitpincurrency',
            name='buy_sell_commission_type',
            field=models.CharField(choices=[('value', 'Value'), ('percent', 'Percent')], default='percent', max_length=10, verbose_name='Buy Sell Commission Type'),
        ),
    ]