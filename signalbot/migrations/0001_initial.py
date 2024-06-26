# Generated by Django 4.2.3 on 2023-09-13 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TradeSignals",
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
                ("symbol", models.CharField(max_length=255)),
                ("trade_side", models.CharField(max_length=255)),
                ("position_amount", models.FloatField()),
                ("leverage", models.FloatField()),
                ("trailing_stop_percent", models.FloatField()),
                ("take_profit_percent", models.FloatField()),
            ],
        ),
    ]
