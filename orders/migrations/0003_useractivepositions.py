# Generated by Django 4.2.5 on 2024-05-03 03:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("signalbot", "0019_signalfollowedby_first_order_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "orders",
            "0002_remove_order_price_order_avg_price_order_entry_price_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="UserActivePositions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "entry_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "mark_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "liquidationPrice",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "breakEvenPrice",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "marginRatio",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "margin",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "margin_percentage",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "pnl",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "pnl_percentage",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("date_time", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "symbol",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="signalbot.tradesymbol",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]