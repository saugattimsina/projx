# Generated by Django 4.2.5 on 2024-05-17 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_usersubcription_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='description',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='package_type',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='time_in_days',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='time_in_months',
        ),
        migrations.DeleteModel(
            name='SubscriptionDetail',
        ),
    ]
