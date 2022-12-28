from django.db import models
import datetime

class Person(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(null=True)
    time = models.DateTimeField(null=True)
    closest_position = models.CharField(max_length=100, null=True)
    closest_distance = models.FloatField(max_length=100, null=True)

    def __str__(self):
        return self.name
