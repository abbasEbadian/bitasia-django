# Generated by Django 4.2.8 on 2024-04-02 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bitpin', '0006_alter_bitpincurrency_active_and_more'),
        ('order', '0002_order_wallet_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('cancel', 'Cancel'), ('success', 'Success')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=20, verbose_name='Amount')),
                ('track_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Track ID')),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bitpin.bitpincurrency')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Purchase',
                'verbose_name_plural': 'Purchases',
                'ordering': ('-id',),
            },
        ),
    ]