# Generated by Django 4.2.11 on 2024-04-21 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0007_alter_authorityrequest_admin_message_and_more'),
        ('users', '0010_remove_customuser_avatar_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='authority_option_ids',
            field=models.ManyToManyField(to='authority.authorityruleoption'),
        ),
    ]
