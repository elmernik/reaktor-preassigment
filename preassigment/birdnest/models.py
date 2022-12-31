from django.db import models
import datetime

# Create a person model to store the information of the people violating the NDZ
class Person(models.Model):
    name = models.CharField(max_length=100) 
    email = models.CharField(max_length=100, default='first.last@example.com')
    phone_number = models.CharField(max_length=100, default='+123456789')
    time = models.DateTimeField(null=True)
    closest_distance = models.FloatField(max_length=100, null=True)

    def __str__(self):
        return self.name
