# Generated by Django 3.2 on 2023-05-06 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0002_analyzerun_number_of_analyzed_fvids'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyzerun',
            name='number_of_analyzed_matrices',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
