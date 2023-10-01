# Generated by Django 4.2.5 on 2023-10-01 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('binarytree', '0005_mlmrank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlmrank',
            name='referrals',
        ),
        migrations.RemoveField(
            model_name='mlmrank',
            name='team_size',
        ),
        migrations.AddField(
            model_name='mlmrank',
            name='max_referrals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mlmrank',
            name='max_team_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mlmrank',
            name='min_referrals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mlmrank',
            name='min_team_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='binarytree.mlmrank')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
