# Generated by Django 4.2.5 on 2023-10-12 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signalbot', '0013_remove_referalincome_is_withdrawn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referalwallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]