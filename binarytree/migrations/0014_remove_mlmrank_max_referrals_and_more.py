# Generated by Django 4.2.5 on 2024-04-22 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("binarytree", "0013_alter_mlmrank_equivalent_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mlmrank",
            name="max_referrals",
        ),
        migrations.RemoveField(
            model_name="mlmrank",
            name="max_team_size",
        ),
        migrations.RemoveField(
            model_name="mlmrank",
            name="min_referrals",
        ),
        migrations.RemoveField(
            model_name="mlmrank",
            name="min_team_size",
        ),
        migrations.AddField(
            model_name="mlmrank",
            name="active_members",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="mlmrank",
            name="direct_referrals",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="mlmrank",
            name="separate_enroller_tree_conditions",
            field=models.JSONField(default={}),
        ),
    ]
