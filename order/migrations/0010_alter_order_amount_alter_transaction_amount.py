# Generated by Django 4.2.11 on 2024-04-19 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_transaction_amount_after_commission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=9, max_digits=20, verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=9, max_digits=20, verbose_name='مقدار'),
        ),
    ]
