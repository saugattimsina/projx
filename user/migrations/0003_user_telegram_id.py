# Generated by Django 4.2.3 on 2023-09-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_user_user_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="telegram_id",
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
