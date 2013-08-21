import scraperwiki
import urllib2
import csv
import string

import scraperwiki

URL = "http://www.manchester.gov.uk/download/14320/public_toilets"
ONS_CODE = "E08000003"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = line['Where'].strip().split(',')[0].split(':')[0]
    cleaned_data['address'] = line['Where'].strip()

    lat_lng = line['Location'].split(',')
    cleaned_data['WGS84_lat'] = lat_lng[0].strip()
    cleaned_data['WGS84_long'] = lat_lng[1].strip()

    #Horrid Hack
    cleaned_data['postcode'] = cleaned_data['address']

    scraperwiki.sqlite.save(unique_keys=['name','address'], data=cleaned_data)  

