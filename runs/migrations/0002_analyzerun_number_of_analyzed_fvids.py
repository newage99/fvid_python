# Generated by Django 3.2 on 2022-05-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyzerun',
            name='number_of_analyzed_fvids',
            field=models.PositiveIntegerField(default=0),
        ),
    ]