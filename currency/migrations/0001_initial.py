# Generated by Django 4.2.8 on 2024-02-10 15:41

import currency.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(verbose_name='Name')),
                ('symbol', models.CharField(verbose_name='Symbol')),
                ('icon', models.ImageField(upload_to=currency.models.get_file_path_for_icon, verbose_name='Icon')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
    ]