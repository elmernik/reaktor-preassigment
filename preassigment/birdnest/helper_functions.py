import urllib3
import xmltodict

# Get the xml data of the drones and convert it to a dictionary
def getxml():
    url = 'https://assignments.reaktor.com/birdnest/drones'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    return data