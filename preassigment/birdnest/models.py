from django.db import models
import datetime

class Person(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    last_seen = datetime.datetime.now()
    closest_position = models.CharField(max_length=100)

    def __str__(self):
        return self.name
