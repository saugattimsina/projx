# Generated by Django 4.2.3 on 2023-10-10 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signalbot", "0009_tradehistory_portfolio"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="stop_price",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="portfolio",
            name="take_profit_price",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="tradehistory",
            name="symbol",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
