# Generated by Django 4.2.5 on 2023-10-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_base32',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]