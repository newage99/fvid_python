# Generated by Django 3.2 on 2022-05-09 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FVID',
            fields=[
                ('value', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
    ]
