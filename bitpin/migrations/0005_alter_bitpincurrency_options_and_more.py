# Generated by Django 4.2.8 on 2024-04-01 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpin', '0001_squashed_0004_bitpincurrency_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bitpincurrency',
            options={'ordering': ('id',), 'verbose_name': 'Currency', 'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='bitpinnetwork',
            options={'verbose_name': 'Network', 'verbose_name_plural': 'Networks'},
        ),
        migrations.AddField(
            model_name='bitpincurrency',
            name='bitasia_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]