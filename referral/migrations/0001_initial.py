# Generated by Django 4.2.11 on 2024-04-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('min_subset_count', models.IntegerField()),
                ('max_subset_count', models.IntegerField()),
                ('percent', models.FloatField()),
            ],
            options={
                'verbose_name': 'Referral Program',
                'verbose_name_plural': 'Referral Programs',
            },
        ),
    ]
