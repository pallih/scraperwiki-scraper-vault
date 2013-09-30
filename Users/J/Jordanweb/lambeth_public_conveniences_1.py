import urllib2
import re
import csv

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

URL = "http://www.lambeth.gov.uk/NR/rdonlyres/CD4605F5-339E-498A-97A1-FBE23B845627/0/LambethPublicConveniences.csv"
ONS_CODE = "E09000022"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = line['BUILDING_NAME']
    

    cleaned_data['address'] = line['BUILDING_NAME']
    
    
        
    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['EASTING'], line['NORTHING'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    cleaned_data['name'] = cleaned_data['name'].decode('latin1')

    
    cleaned_data['postcode'] = line['BUILDING_NAME']

    

    scraperwiki.sqlite.save(unique_keys=['address', 'name',], data=cleaned_data)    
import urllib2
import re
import csv

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

URL = "http://www.lambeth.gov.uk/NR/rdonlyres/CD4605F5-339E-498A-97A1-FBE23B845627/0/LambethPublicConveniences.csv"
ONS_CODE = "E09000022"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = line['BUILDING_NAME']
    

    cleaned_data['address'] = line['BUILDING_NAME']
    
    
        
    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['EASTING'], line['NORTHING'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    cleaned_data['name'] = cleaned_data['name'].decode('latin1')

    
    cleaned_data['postcode'] = line['BUILDING_NAME']

    

    scraperwiki.sqlite.save(unique_keys=['address', 'name',], data=cleaned_data)    
