# Generated by Django 4.2.8 on 2024-02-11 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RialDeposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='Amount')),
                ('factor_number', models.CharField(unique=True, verbose_name='Factor number')),
                ('gateway_token', models.CharField(blank=True, help_text='Authority', null=True, verbose_name='Gateway Token')),
                ('gateway_status', models.CharField(blank=True, null=True, verbose_name='Gateway Status')),
                ('gateway_fee', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, verbose_name='Gateway Fee')),
                ('gateway_fee_type', models.CharField(blank=True, null=True, verbose_name='Gateway Fee Type')),
                ('gateway_message', models.CharField(blank=True, null=True, verbose_name='Gateway Message')),
                ('card_number', models.CharField(max_length=16, verbose_name='Card Number')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('cancel', 'Cancel')], default='pending', verbose_name='Status')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rial deposit',
                'verbose_name_plural': 'Rial deposits',
            },
        ),
        migrations.CreateModel(
            name='VerifyLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('ref_id', models.CharField(blank=True, null=True, verbose_name='Verify Ref ID')),
                ('message', models.CharField(blank=True, null=True, verbose_name='Verify message')),
                ('status', models.CharField(blank=True, null=True, verbose_name='Verify status')),
                ('result', models.CharField(choices=[('ok', 'OK'), ('nok', 'NOK')], default='nok', verbose_name='Result')),
                ('card_pan', models.CharField(blank=True, null=True, verbose_name='Card')),
                ('card_hash', models.CharField(blank=True, null=True, verbose_name='Card Hash')),
                ('fee_type', models.CharField(blank=True, null=True, verbose_name='Fee Type')),
                ('fee', models.FloatField(blank=True, null=True, verbose_name='Fee')),
                ('deposit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zarinpal.rialdeposit')),
            ],
            options={
                'verbose_name': 'Verify Deposit Attempt',
                'verbose_name_plural': 'Verify Deposit Attempts',
            },
        ),
    ]
