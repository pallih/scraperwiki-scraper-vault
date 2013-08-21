import scraperwiki
import requests
from BeautifulSoup import BeautifulStoneSoup

"""
bbox is the bounding box for the selected area. The first coordinate pair is the lower left corner and the second upper right
The last element is the Map Feature: http://wiki.openstreetmap.org/wiki/Map_Features#Sustenance
"""

url = "http://www.overpass-api.de/api/xapi?node[bbox=5.604348,47.283615,14.930526,54.935681][amenity=fuel]"
xml = requests.get(url, verify = False).text

soup = BeautifulStoneSoup(xml)
nodes = soup.findAll('node')

for node in nodes:
    
    id = node['id']
    lat = node['lat']
    lon = node['lon']

    try:
        street = node('tag', k = 'addr:street')[0]['v']
    except IndexError:
        street = None

    try:
        houseNumber= node('tag', k = 'addr:housenumber')[0]['v']
    except IndexError:
        houseNumber = None

    try:
        postcode = node('tag', k = 'addr:postcode')[0]['v']
    except IndexError:
        postcode = None

    try:
        city = node('tag', k = 'addr:city')[0]['v']
    except IndexError:
        city = None

    try:
        country = node('tag', k = 'addr:country')[0]['v']
    except IndexError:
        country = None

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

        data = {'id' : id,
        'lat' : lat,
        'lon' : lon,
        'name' : name,
        'street' : street,
        'houseNumber' : houseNumber,
        'postcode' : postcode,
        'city' : city,
        'country' : country,  
        'phone' : phone,
        'website' : website
        }  

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    


