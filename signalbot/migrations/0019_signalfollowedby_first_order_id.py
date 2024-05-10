# Generated by Django 4.2.5 on 2024-04-30 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "orders",
            "0002_remove_order_price_order_avg_price_order_entry_price_and_more",
        ),
        ("signalbot", "0018_tradehistory_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="signalfollowedby",
            name="first_order_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="orders.order",
            ),
        ),
    ]