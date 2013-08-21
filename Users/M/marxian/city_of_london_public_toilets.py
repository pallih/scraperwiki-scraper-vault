import urllib2
import re
import hashlib

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

KML_URL ="http://apps.cityoflondon.gov.uk/community-toilets/toilets_live.kml"
ONS_CODE = "E09000001"

soup = BeautifulStoneSoup(urllib2.urlopen(KML_URL))
for toilet in soup.findAll('placemark'):

    cleaned_data = {'ons_code' : ONS_CODE}

    # Clean up name 
    toilet_name = toilet.find('name').string.strip()
    cleaned_data['name'] = toilet_name
    
    # Get the location

    cleaned_data['WGS84_long'] = toilet.find('point').find('coordinates').string.split(',')[0].strip()
    cleaned_data['WGS84_lat'] = toilet.find('point').find('coordinates').string.split(',')[1].strip()

    # horrid hack
    cleaned_data['postcode'] = toilet_name.lower()


    cleaned_data['toilet_id'] = hashlib.sha224(toilet_name + cleaned_data['WGS84_lat']).hexdigest()

    scraperwiki.sqlite.save(unique_keys=['WGS84_lat', 'WGS84_long', 'name',], data=cleaned_data)    
    
    
