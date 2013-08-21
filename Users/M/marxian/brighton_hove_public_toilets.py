import urllib2
import re
import md5

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

import scraperwiki

KML_URL = "http://www.brighton-hove.gov.uk/downloads/bhcc/openData/mapFiles/PublicToiletsKML.kml"
ONS_CODE = "E06000043"

soup = BeautifulStoneSoup(urllib2.urlopen(KML_URL))
for toilet in soup.findAll('placemark'):

    cleaned_data = {'ons_code' : ONS_CODE}

    # Clean up name 
    toilet_name = toilet.find('name').string
    if toilet_name.startswith('Public toilet'):
        toilet_name = toilet_name[len('Public toilet'):]
    toilet_name = re.sub("^[^A-Z]+", "", toilet_name)
    cleaned_data['name'] = toilet_name
    
    # Get the location
    location = toilet.find('coordinates').string.split(',')
    cleaned_data['WGS84_lat'] = location[1]
    cleaned_data['WGS84_long'] = location[0]

    # We require a postcode - though it doesn't have to be a postcode
    # Horrid Hack!
    cleaned_data['postcode'] = toilet_name
    
    #Address
    cleaned_data['address'] = toilet_name


    # Parse out the CDATA in the description
    #descriptionSoup = BeautifulSoup(toilet.find('description').string)
    #more_info_url = descriptionSoup.find('a')['href']
    
    # Parse the more info url for address and extra information.
    # TODO: There is more data on this page that will not be parsed for the time being.
    # This includes opening times and facilities
    
    #page_soup = BeautifulSoup(urllib2.urlopen(more_info_url),convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    #address = ''.join(page_soup.find('strong', text="Address:").next.findAll(text=True))
    #post_code = address.split(',')[-1].strip()
    #address = ', '.join([s.strip() for s in address.split(',')[:-1]])

    # Ugly use of .next.next here to skip over a spurious <br>
    #cleaned_data['babychanging'] = ('Yes' in page_soup.find('strong', text="Baby changing facilities:").next.next)
    #cleaned_data['disabled'] = ('Yes' in page_soup.find('strong', text="Disabled facilities:").next.next)
    #cleaned_data['opening'] = page_soup.find('strong', text="Hours of operation:").next.next
    
    #cleaned_data['postcode'] = post_code
    #cleaned_data['address'] = address
    cleaned_data['toilet_id'] = md5.md5(toilet_name + ' Brighton and Hove').hexdigest()

    scraperwiki.sqlite.save(unique_keys=['toilet_id'], data=cleaned_data)    
    