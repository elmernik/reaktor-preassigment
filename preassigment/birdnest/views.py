from django.shortcuts import render
import requests
from birdnest.models import Person
from datetime import datetime, timedelta
import math
import pytz
import urllib3
import xmltodict

# Get the xml data of the drones and convert it to a dictionary
def getxml():
    url = 'https://assignments.reaktor.com/birdnest/drones'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    return data

def index(request):
    # Get a dictionary containing the xml data
    xmldict = getxml() 
    # Get a list of the relevant drone info
    drones = [i for i in xmldict['report']['capture']['drone']]

    drones_inside_zone = []

    # Create a list of drones inside the zone storing tuples of relevant data, drone distance and position
    for drone in drones:
        distance = pow(float(drone['positionX']) - 250000, 2) + pow(float(drone['positionY']) - 250000, 2)
        if distance < pow(100000, 2):
            drones_inside_zone.append((drone, distance, drone['positionX'] +  ' ' + drone['positionY']))

    for drone, distance, position in drones_inside_zone:
        # Get the information of the person whose drone it is
        response = requests.get('https://assignments.reaktor.com/birdnest/pilots/' + drone['serialNumber'])
        data = response.json()

        # Check if person is in database
        if Person.objects.filter(name=(data['firstName'] + ' ' + data['lastName'])):
            person = Person.objects.get(name=(data['firstName'] + ' ' + data['lastName']))
            # If person in database then check if the new distance is closer than the old one
            closest_distance = round(math.sqrt(distance)/1000, 2) if person.closest_distance > round(math.sqrt(distance)/1000, 2) else person.closest_distance
        else:
            # If not in database new distance is closest
            closest_distance = round(math.sqrt(distance)/1000, 2)

        # Update or create the person to the NDZ violators database
        Person.objects.update_or_create(name=(data['firstName'] + ' ' + data['lastName']), defaults=dict(email=data['email'], phone_number=data['phoneNumber'], time=datetime.now(pytz.timezone('Europe/Helsinki')), closest_distance=closest_distance))

    # Remove all people from the database who haven'nt been seen in 10 minutes
    Person.objects.filter(time__lte=datetime.now(pytz.timezone('Europe/Helsinki')) - timedelta(minutes=10)).delete()

    # Render the people to a list on the page
    return render(request, 'index.html', {'people': Person.objects.all()})

