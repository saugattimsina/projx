# Generated by Django 4.2.3 on 2023-10-11 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_user_otp_base32'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_first_month',
            field=models.BooleanField(default=True),
        ),
    ]
