import json
import time 
from googlemaps import GoogleMaps
import scraperwiki
import urllib  
import StringIO
import csv

txt = urllib.urlopen("https://dl.dropbox.com/u/49328567/impressions_mini.txt")


counter = 0
for i in range(1500): 
    new_line = txt.readline() 
    new_json = json.loads(new_line)
    date     = new_json['sdate']['$date']
    hour     =  time.gmtime(date/1000).tm_hour + 1 
    data = {"ID" : counter, "date": hour, "lat": new_json['lat'], "lon": new_json['lon']} 
    counter += 1 
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)

import json
import time 
from googlemaps import GoogleMaps
import scraperwiki
import urllib  
import StringIO
import csv

txt = urllib.urlopen("https://dl.dropbox.com/u/49328567/impressions_mini.txt")


counter = 0
for i in range(1500): 
    new_line = txt.readline() 
    new_json = json.loads(new_line)
    date     = new_json['sdate']['$date']
    hour     =  time.gmtime(date/1000).tm_hour + 1 
    data = {"ID" : counter, "date": hour, "lat": new_json['lat'], "lon": new_json['lon']} 
    counter += 1 
    scraperwiki.sqlite.save(unique_keys=['ID'], data=data)

