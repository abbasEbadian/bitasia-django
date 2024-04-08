# Generated by Django 4.2.11 on 2024-04-08 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bitpin', '0014_alter_bitpincurrency_options'),
        ('order', '0002_transaction_currency_current_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=8, verbose_name='Transaction Type')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approve', 'Approve'), ('cancel', 'Cancel'), ('reject', 'REJECT')], default='pending', max_length=10)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=20, verbose_name='Amount')),
                ('submit_date', models.DateTimeField(blank=True, null=True, verbose_name='Submit Date')),
                ('currency_current_value', models.PositiveBigIntegerField(default=0, verbose_name='The irt price at the time of placing the ordering.')),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bitpin.bitpincurrency')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ترتیب:',
                'verbose_name_plural': 'Orders',
                'ordering': ('-id',),
            },
        ),
    ]
