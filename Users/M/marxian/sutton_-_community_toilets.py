import urllib2
import re
import csv
from geopy import geocoders

import scraperwiki

URL = "http://www.sutton.gov.uk/CHttpHandler.ashx?id=15909&p=0"
ONS_CODE = "E09000029"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    try:
        cleaned_data = {'ons_code' : ONS_CODE}
        cleaned_data['name'] = line['Premises'].strip()
    
        cleaned_data['address'] = []
        cleaned_data['address'].append(line['Premises'].strip())
        cleaned_data['address'].append(line['Address 1'].strip())
        cleaned_data['address'].append(line['City'].strip())
        cleaned_data['address'].append(line['Post Code'].strip())
        cleaned_data['address'] = ", ".join(cleaned_data['address'])

        cleaned_data['postcode'] = line['Post Code'].strip()

        cleaned_data['babychanging'] = ('Yes' in line['Baby Changing'])
        cleaned_data['disabled'] = ('Yes' in line['Disabled'])

        # Perform Geocode
    
        g = geocoders.Google(domain='maps.google.co.uk')    
        place, (lat, lng) = g.geocode(cleaned_data['postcode'])
        cleaned_data['WGS84_lat'] = lat
        cleaned_data['WGS84_long'] = lng

        scraperwiki.sqlite.save(unique_keys=['address', 'name'], data=cleaned_data) 
    except:
        pass   
import urllib2
import re
import csv
from geopy import geocoders

import scraperwiki

URL = "http://www.sutton.gov.uk/CHttpHandler.ashx?id=15909&p=0"
ONS_CODE = "E09000029"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    try:
        cleaned_data = {'ons_code' : ONS_CODE}
        cleaned_data['name'] = line['Premises'].strip()
    
        cleaned_data['address'] = []
        cleaned_data['address'].append(line['Premises'].strip())
        cleaned_data['address'].append(line['Address 1'].strip())
        cleaned_data['address'].append(line['City'].strip())
        cleaned_data['address'].append(line['Post Code'].strip())
        cleaned_data['address'] = ", ".join(cleaned_data['address'])

        cleaned_data['postcode'] = line['Post Code'].strip()

        cleaned_data['babychanging'] = ('Yes' in line['Baby Changing'])
        cleaned_data['disabled'] = ('Yes' in line['Disabled'])

        # Perform Geocode
    
        g = geocoders.Google(domain='maps.google.co.uk')    
        place, (lat, lng) = g.geocode(cleaned_data['postcode'])
        cleaned_data['WGS84_lat'] = lat
        cleaned_data['WGS84_long'] = lng

        scraperwiki.sqlite.save(unique_keys=['address', 'name'], data=cleaned_data) 
    except:
        pass   
