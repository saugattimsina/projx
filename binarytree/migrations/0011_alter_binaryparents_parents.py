# Generated by Django 4.2.3 on 2023-11-02 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binarytree', '0010_remove_mlmrank_name_mlmrank_equivalent_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binaryparents',
            name='parents',
            field=models.ManyToManyField(blank=True, null=True, to='binarytree.mlmbinary'),
        ),
    ]
