# Generated by Django 4.2.3 on 2023-09-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0002_usersubpaymenthistory_remaining_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersubpaymenthistory",
            name="has_partial_payment",
            field=models.BooleanField(default=False),
        ),
    ]
