# Generated by Django 4.2.8 on 2024-04-01 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitpin', '0005_alter_bitpincurrency_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitpincurrency',
            name='active',
            field=models.BooleanField(default=True, verbose_name='BitPin Active'),
        ),
        migrations.AlterField(
            model_name='bitpincurrency',
            name='bitasia_active',
            field=models.BooleanField(default=True, verbose_name='Bitasia Active'),
        ),
    ]