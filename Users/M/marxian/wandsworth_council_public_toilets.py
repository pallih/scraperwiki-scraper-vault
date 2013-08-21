import urllib2
import re
import csv

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

URL = "http://www.wandsworth.gov.uk/download/4116/public_and_community_toilet_locations_version_2"
ONS_CODE = "E09000032"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    service_provider = line['Service_Provider'].split('-', 1)
    cleaned_data['name'] = service_provider.pop(0).strip()
    
    cleaned_data['address'] = [x.strip() for x in service_provider]
    

    cleaned_data['address'].append(line['Area'])
    cleaned_data['address'] = ", ".join(cleaned_data['address'])
        
    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['X'], line['Y'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]
    cleaned_data['postcode'] = line['Postcode']
    cleaned_data['name'] = cleaned_data['name'].decode('latin1')

    # Extra Data
    opening = []
    # NB source data can't spell Tuesday
    for day in ['Monday','Tueday','Wednesday','Thursday','Friday','Saturday','Sunday']:
        if line.get('Opening_Hours_' + day, False):
            opening.append(day[:3] + ': ' + line['Opening_Hours_' + day])
    if len(opening):
        cleaned_data['opening'] = ', '.join(opening)
    cleaned_data['disabled'] = line['Disabled'].strip() == 'YES' and True or False
    
    cleaned_data['type'] = line['Type'].strip()


    scraperwiki.sqlite.save(unique_keys=['address','postcode'], data=cleaned_data)    
    
