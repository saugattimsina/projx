# Generated by Django 4.2.5 on 2024-04-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0017_user_email_otp_verified"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="email_otp_verified",
            new_name="email_is_verified",
        ),
        migrations.AlterField(
            model_name="user",
            name="email_otp",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
