import urllib2
import re

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

KML_URL = "http://www.richmond.gov.uk/lbrmapfeed.xml?cat=CommunityToilets"
ONS_CODE = "E09000027"

soup = BeautifulStoneSoup(urllib2.urlopen(KML_URL))
for toilet in soup.findAll('location'):

    cleaned_data = {'ons_code' : ONS_CODE}

    # Clean up name 
    toilet_name = toilet.find('title').string
    cleaned_data['name'] = toilet_name
    
    # Get the location

    cleaned_data['WGS84_lat'] = toilet.find('lat').string
    cleaned_data['WGS84_long'] = toilet.find('long').string


    # Ugly use of .next.next here to skip over a spurious <br>
    cleaned_data['babychanging'] = toilet.find('extra2').contents and ('Baby' in toilet.find('extra2').contents[1].string) or False
    cleaned_data['disabled'] = toilet.find('extra2').contents and ('Disabled' in toilet.find('extra2').contents[1].string) or False
    #cleaned_data['opening'] = page_soup.find('strong', text="Hours of operation:").next.next
    
    cleaned_data['postcode'] = toilet.find('postcode').string
    cleaned_data['address'] = toilet.find('address1').string
    cleaned_data['toilet_id'] = toilet.find('id').string

    scraperwiki.sqlite.save(unique_keys=['postcode', 'name',], data=cleaned_data)    
    
    
