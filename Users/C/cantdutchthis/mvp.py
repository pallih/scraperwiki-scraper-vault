import time 
from googlemaps import GoogleMaps
import scraperwiki
import urllib 
import pandas 
import StringIO
import csv

db = urllib.urlopen("http://dl.dropbox.com/u/49328567/location_time_db.csv")
API_KEY             = 'AIzaSyAMENagyIuZzR29ND1NxqQdFSxS9chJW9w' 
gmaps                 = GoogleMaps(API_KEY)
f = StringIO.StringIO(db.read())
reader = csv.reader(f, delimiter=';')

counter = 0 
for row in reader: 
    time.sleep(0.5) 
    adres = row[1] + " " + row[2]
    lat, lng          = gmaps.address_to_latlng(adres)
    data = {"ID" : counter, "tijd": row[0], "adres": adres, "lat": lat, "lon": lng}
    counter += 1
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)

