# Generated by Django 4.2.3 on 2023-10-13 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_is_first_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_connected_to_authunticator',
            field=models.BooleanField(default=False),
        ),
    ]