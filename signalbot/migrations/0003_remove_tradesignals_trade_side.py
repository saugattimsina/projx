# Generated by Django 4.2.3 on 2023-09-15 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("signalbot", "0002_rename_leverage_tradesignals_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tradesignals",
            name="trade_side",
        ),
    ]
