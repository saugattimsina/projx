# Generated by Django 4.2.5 on 2024-04-09 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0015_user_email_otp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram_id",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
