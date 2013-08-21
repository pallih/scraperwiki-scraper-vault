import csv
import urllib2
import json

import scraperwiki

CSV_URL = "http://www.lincoln.gov.uk/doclib/Lincoln_Public_Toilets.csv"
ONS_CODE = "E07000138"
 
data = csv.DictReader(urllib2.urlopen(CSV_URL))
for toilet in data:
    cleaned_data = {'ons_code' : ONS_CODE}
    cleaned_data['name'] = toilet['Toilet']
    post_code = toilet['Nearest post code'].replace(' ', '')
    cleaned_data['postcode'] = post_code
    
    geolocated = json.loads(scraperwiki.scrape("http://scraperwikiviews.com/run/uk_postcode_lookup/?postcode=%s" % post_code))
    cleaned_data['WGS84_lat'] = geolocated['lat']
    cleaned_data['WGS84_long'] = geolocated['lng']

    cleaned_data['address'] = ', '.join([toilet['Location'].strip(), post_code])

    
    cleaned_data['disabled'] = toilet['Disabled'].strip() == 'NO' and False or True
    cleaned_data['opening'] = toilet['Opening times'].strip()
    cleaned_data['babychanging'] = toilet['Baby change'].strip() == 'No' and False or True

    
    scraperwiki.sqlite.save(unique_keys=['postcode', 'name',], data=cleaned_data)