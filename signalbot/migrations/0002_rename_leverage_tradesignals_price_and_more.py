# Generated by Django 4.2.3 on 2023-09-15 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signalbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tradesignals',
            old_name='leverage',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='tradesignals',
            old_name='position_amount',
            new_name='stop_amount',
        ),
        migrations.RenameField(
            model_name='tradesignals',
            old_name='take_profit_percent',
            new_name='take_profit_amount',
        ),
        migrations.RemoveField(
            model_name='tradesignals',
            name='trailing_stop_percent',
        ),
    ]
