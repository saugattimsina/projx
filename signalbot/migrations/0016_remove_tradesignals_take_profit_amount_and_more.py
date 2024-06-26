# Generated by Django 4.2.5 on 2023-10-13 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signalbot", "0015_merge_20231013_1718"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tradesignals",
            name="take_profit_amount",
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="amount_1",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="amount_2",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="amount_3",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="amount_4",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="percentage_1",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="percentage_2",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="percentage_3",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tradesignals",
            name="percentage_4",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="TakeProfits",
        ),
    ]
