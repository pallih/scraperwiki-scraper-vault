import scraperwiki
import urllib2
import csv
import string

import scraperwiki

URL = "http://publicloo.neontribe.co.uk/data/hackney_public_toilets.csv"
ONS_CODE = "E09000012"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = string.capwords(line['PAON'].strip())
    cleaned_data['address'] = string.capwords(', '.join([line['STREET_DESCRIPTOR'].strip(), 'Hackney']))

    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['X_COORDINATE'], line['Y_COORDINATE'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    #Horrid Hack
    cleaned_data['postcode'] = cleaned_data['address']

    scraperwiki.sqlite.save(unique_keys=['name','address'], data=cleaned_data)  

import scraperwiki
import urllib2
import csv
import string

import scraperwiki

URL = "http://publicloo.neontribe.co.uk/data/hackney_public_toilets.csv"
ONS_CODE = "E09000012"

csv_file = csv.DictReader(urllib2.urlopen(URL))
for line in csv_file:
    cleaned_data = {'ons_code' : ONS_CODE}
    
    cleaned_data['name'] = string.capwords(line['PAON'].strip())
    cleaned_data['address'] = string.capwords(', '.join([line['STREET_DESCRIPTOR'].strip(), 'Hackney']))

    lat_lng = scraperwiki.geo.os_easting_northing_to_latlng(*map(float, (line['X_COORDINATE'], line['Y_COORDINATE'],)))
    cleaned_data['WGS84_lat'] = lat_lng[0]
    cleaned_data['WGS84_long'] = lat_lng[1]

    #Horrid Hack
    cleaned_data['postcode'] = cleaned_data['address']

    scraperwiki.sqlite.save(unique_keys=['name','address'], data=cleaned_data)  

