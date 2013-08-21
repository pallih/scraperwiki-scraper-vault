import scraperwiki
import requests
from BeautifulSoup import BeautifulStoneSoup

"""
bbox is the bounding box for the selected area. The first coordinate pair is the lower left corner and the second upper right
The last element is the Map Feature: http://wiki.openstreetmap.org/wiki/Map_Features#Sustenance
"""

url = "http://www.overpass-api.de/api/xapi?node[bbox=5.87,47.27,15.04,55.12][shop=bakery]"
xml = requests.get(url, verify = False).text

soup = BeautifulStoneSoup(xml)
nodes = soup.findAll('node')

for node in nodes:
    
    id = node['id']
    lat = node['lat']
    lon = node['lon']

    try:
        houseNumber= node('tag', k = 'addr:housenumber')[0]['v']
    except IndexError:
        houseNumber = None

    try:
        street = node('tag', k = 'addr:street')[0]['v']
    except IndexError:
        street = None

    try:
        name = node('tag', k = 'name')[0]['v']
    except IndexError:
        name = None

    try:
        website = node('tag', k = 'website')[0]['v']
    except IndexError:
        website = None

    try:
        phone = node('tag', k = 'phone')[0]['v']
    except IndexError:
        phone = None

    try:
        openingHours = node('tag', k = 'opening_hours')[0]['v']
    except IndexError:
        openingHours = None

    try:
        postcode = node('tag', k = 'addr:postcode')[0]['v']
    except IndexError:
        postcode = None

    try:
        city = node('tag', k = 'addr:city')[0]['v']
    except IndexError:
        city = None


        data = {'id' : id,
        'name' : name,
        'lat' : lat,
        'lon' : lon,
        'website' : website,
        'street' : street,
        'houseNumber' : houseNumber,
        'postcode' : postcode,
        'city' : city,
        'phone': phone,
        'openingHours' : openingHours}  

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
      
      
    


import scraperwiki
import requests
from BeautifulSoup import BeautifulStoneSoup

"""
bbox is the bounding box for the selected area. The first coordinate pair is the lower left corner and the second upper right
The last element is the Map Feature: http://wiki.openstreetmap.org/wiki/Map_Features#Sustenance
"""

url = "http://www.overpass-api.de/api/xapi?node[bbox=5.87,47.27,15.04,55.12][shop=bakery]"
xml = requests.get(url, verify = False).text

soup = BeautifulStoneSoup(xml)
nodes = soup.findAll('node')

for node in nodes:
    
    id = node['id']
    lat = node['lat']
    lon = node['lon']

    try:
        houseNumber= node('tag', k = 'addr:housenumber')[0]['v']
    except IndexError:
        houseNumber = None

    try:
        street = node('tag', k = 'addr:street')[0]['v']
    except IndexError:
        street = None

    try:
        name = node('tag', k = 'name')[0]['v']
    except IndexError:
        name = None

    try:
        website = node('tag', k = 'website')[0]['v']
    except IndexError:
        website = None

    try:
        phone = node('tag', k = 'phone')[0]['v']
    except IndexError:
        phone = None

    try:
        openingHours = node('tag', k = 'opening_hours')[0]['v']
    except IndexError:
        openingHours = None

    try:
        postcode = node('tag', k = 'addr:postcode')[0]['v']
    except IndexError:
        postcode = None

    try:
        city = node('tag', k = 'addr:city')[0]['v']
    except IndexError:
        city = None


        data = {'id' : id,
        'name' : name,
        'lat' : lat,
        'lon' : lon,
        'website' : website,
        'street' : street,
        'houseNumber' : houseNumber,
        'postcode' : postcode,
        'city' : city,
        'phone': phone,
        'openingHours' : openingHours}  

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
      
      
    


