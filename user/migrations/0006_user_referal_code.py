# Generated by Django 4.2.3 on 2023-09-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_user_telegram_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="referal_code",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
