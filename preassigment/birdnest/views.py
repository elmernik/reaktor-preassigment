from django.shortcuts import render
from django.http import HttpResponse
import requests
import urllib3
import xmltodict
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
    people = []

    for drone in drones:
        if pow(float(drone['positionX']) - 250000, 2) + pow(float(drone['positionY']) - 250000, 2) < pow(100000, 2):
            drones_inside_zone.append(drone)

    for drone in drones_inside_zone:
        response = requests.get('https://assignments.reaktor.com/birdnest/pilots/' + drone['serialNumber'])
        people.append(response.json())

    return render(request, 'index.html', {'people': people})

