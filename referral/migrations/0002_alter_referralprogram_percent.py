# Generated by Django 4.2.11 on 2024-04-23 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralprogram',
            name='percent',
            field=models.DecimalField(decimal_places=0, max_digits=3),
        ),
    ]
