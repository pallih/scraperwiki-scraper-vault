import urllib2
import re
import csv
from geopy import geocoders

import scraperwiki

URL = "http://publicloo.neontribe.co.uk/data/national_rail_toilets.csv"
ONS_CODE = "NR1"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    if line['TOILET'] == 'yes':
        try:
            cleaned_data = {'ons_code' : ONS_CODE}
            name = line['NAME'].strip() + ' Station'
            cleaned_data['name'] = name
    
            cleaned_data['address'] = name
        
            # Hack
            cleaned_data['postcode'] = name

            cleaned_data['WGS84_lat'] = line['LAT']
            cleaned_data['WGS84_long'] = line['LON']

            scraperwiki.sqlite.save(unique_keys=['name'], data=cleaned_data) 
        except:
            pass   
