import urllib2
import re
import csv

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

URL = "http://www.lambeth.gov.uk/NR/rdonlyres/946C2CB4-34B0-4260-A4A4-7AEE3BED602D/0/LambethCommunityToilets.csv"
ONS_CODE = "E09000022"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = line['NAME']
    

    cleaned_data['address'] = line['ADDRESS']
    
    
        
    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['X'], line['Y'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    cleaned_data['name'] = cleaned_data['name'].decode('latin1')

    
    cleaned_data['postcode'] = line['POSTCODE']

    # Extra Data
    cleaned_data['opening'] = line['OPENING_HOURS']
    cleaned_data['babychanging'] = ('Baby changing' in line['TOILETS']) and True or False
    cleaned_data['disabled'] = ('Disabled' in line['TOILETS']) and True or False

    scraperwiki.sqlite.save(unique_keys=['address', 'name',], data=cleaned_data)    
import urllib2
import re
import csv

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

URL = "http://www.lambeth.gov.uk/NR/rdonlyres/946C2CB4-34B0-4260-A4A4-7AEE3BED602D/0/LambethCommunityToilets.csv"
ONS_CODE = "E09000022"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = line['NAME']
    

    cleaned_data['address'] = line['ADDRESS']
    
    
        
    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['X'], line['Y'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    cleaned_data['name'] = cleaned_data['name'].decode('latin1')

    
    cleaned_data['postcode'] = line['POSTCODE']

    # Extra Data
    cleaned_data['opening'] = line['OPENING_HOURS']
    cleaned_data['babychanging'] = ('Baby changing' in line['TOILETS']) and True or False
    cleaned_data['disabled'] = ('Disabled' in line['TOILETS']) and True or False

    scraperwiki.sqlite.save(unique_keys=['address', 'name',], data=cleaned_data)    
