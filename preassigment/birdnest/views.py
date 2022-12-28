from django.shortcuts import render
from django.http import HttpResponse
import requests
import urllib3
import xmltodict
from birdnest.models import Person
import datetime

def getxml():
    url = 'https://assignments.reaktor.com/birdnest/drones'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    return data


def index(request):
    xmldict = getxml()
    drones = [i for i in xmldict['report']['capture']['drone']]

    drones_inside_zone = []

    for drone in drones:
        distance = pow(float(drone['positionX']) - 250000, 2) + pow(float(drone['positionY']) - 250000, 2)
        if distance < pow(100000, 2):
            drones_inside_zone.append((drone, distance, drone['positionX'] +  ' ' + drone['positionY']))

    for drone, distance, position in drones_inside_zone:
        response = requests.get('https://assignments.reaktor.com/birdnest/pilots/' + drone['serialNumber'])
        data = response.json()

        if Person.objects.filter(name=(data['firstName'] + ' ' + data['lastName'])):
            person = Person.objects.get(name=(data['firstName'] + ' ' + data['lastName']))
            closest_position = position if person.closest_distance < distance else person.closest_position
            closest_distance = distance if person.closest_distance < distance else person.closest_distance
        else:
            closest_position = position
            closest_distance = distance

        Person.objects.update_or_create(name=(data['firstName'] + ' ' + data['lastName']), defaults=dict(data=data, time=datetime.datetime.now(tz=datetime.timezone.utc), closest_position=closest_position, closest_distance=closest_distance))

    people = Person.objects.filter(time__gte=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=10), time__lte=datetime.datetime.now(tz=datetime.timezone.utc))

    return render(request, 'index.html', {'people': people})

