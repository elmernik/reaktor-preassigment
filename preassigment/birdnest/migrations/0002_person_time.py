# Generated by Django 3.2.16 on 2022-12-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birdnest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]