# Generated by Django 4.2.5 on 2024-04-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0016_alter_user_telegram_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_otp_verified",
            field=models.BooleanField(default=False),
        ),
    ]