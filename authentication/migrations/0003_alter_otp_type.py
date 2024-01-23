# Generated by Django 4.2.8 on 2024-01-21 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_otp_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='type',
            field=models.CharField(choices=[('login', 'ورود'), ('register', 'ثبت نام'), ('password', 'بازیابی رمزعبور'), ('transaction', 'ایجاد تراکنش')], default='login', max_length=20, verbose_name='نوع کدتایید'),
        ),
    ]