# Generated by Django 4.2.8 on 2024-04-01 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'ordering': ('-balance',), 'verbose_name': 'Wallet', 'verbose_name_plural': 'Wallets'},
        ),
    ]