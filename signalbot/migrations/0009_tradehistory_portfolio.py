# Generated by Django 4.2.3 on 2023-10-10 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("signalbot", "0008_signalfollowedby_is_cancelled"),
    ]

    operations = [
        migrations.CreateModel(
            name="TradeHistory",
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
                ("trade_id", models.CharField(blank=True, max_length=255, null=True)),
                ("amount", models.FloatField()),
                ("price", models.FloatField()),
                (
                    "trade_side",
                    models.CharField(
                        choices=[("buy", "buy"), ("sell", "sell")], max_length=255
                    ),
                ),
                ("profit_loss", models.FloatField()),
                ("trade_fee", models.FloatField()),
                ("fee_currency", models.CharField(max_length=255)),
                ("created_on", models.DateTimeField(blank=True, null=True)),
                (
                    "symbol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
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
        migrations.CreateModel(
            name="Portfolio",
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
                ("quantity", models.FloatField()),
                ("entry_price", models.FloatField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "symbol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
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
