# Generated by Django 4.2.8 on 2024-01-21 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_birth_date_customuser_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthdate',
            field=models.CharField(blank=True, null=True, verbose_name='تاریخ تولد'),
        ),
    ]
