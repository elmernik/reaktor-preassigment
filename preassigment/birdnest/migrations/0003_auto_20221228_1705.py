# Generated by Django 3.2.16 on 2022-12-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birdnest', '0002_person_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='closest_distance',
            field=models.FloatField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='closest_position',
            field=models.CharField(max_length=100, null=True),
        ),
    ]