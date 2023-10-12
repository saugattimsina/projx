# Generated by Django 4.2.5 on 2023-10-12 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('binarytree', '0008_binaryparents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binaryparents',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
