# Generated by Django 4.2.3 on 2023-09-22 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubpaymenthistory',
            name='remaining_amount',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True),
        ),
    ]