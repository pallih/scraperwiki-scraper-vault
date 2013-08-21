# Imports!
import lxml.html
import requests
import scraperwiki
from twill.commands import *
#geocoding imports
from scraperwiki import swimport
from scraperwiki.sqlite import attach, select, get_var, save_var, save, execute, commit, show_tables
from urllib2 import urlopen
from urllib import urlencode
from json import loads, dumps
from time import sleep, time
from unidecode import unidecode
from geopy import geocoders, distance
import re
#geocoding class
GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

def geocode_url(address):
    return GEOCODE_URL % urlencode({'q': address})

class geocoder:
    GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&json_callback=&%s'

    def geocode_url(self, address):
        return self.GEOCODE_URL % urlencode({'q': address})

    def load(self, address):
        url = self.geocode_url(address)
        while True:
            try:
                json = urlopen(url).read()
            except:
                d = []
                break
            else:
                d = loads(json)
                break
        
        return d

    @staticmethod
    def convert_coords(coords):
        try:
            return tuple(map(float, coords))
        except TypeError:
            raise TypeError("coords could not be converted to a tuple of latitude and longitude numbers.")

    def geocode(self, address, exactly_one = True):
        d = self.load(unidecode(address))
        if len(d) > 0:
            lat = [(match[u'lat']) for match in d]
            lon = [(match[u'lon']) for match in d]
            arr = [lat,lon]
            return(arr)
        else:
            return None

# end geocoding stuff

# Initialize the scraperwiki/GASP tools.
gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("35c7f25a14624b968eb771c9062ecb30", "S001177")

pdf_dump = scraperwiki.scrape('http://www.bizjournals.com/washington/pdf/Vacant_Exempt_Blight_Aug2011.pdf')
pdf_xml = scraperwiki.pdftoxml(pdf_dump)
pdf_xml_parsed = lxml.html.fromstring(pdf_xml)

pdf_xml_texts = pdf_xml_parsed.xpath("//text[@left='79']")

suffix_strings = {
'ALY':'ALY',
'AVE':'AV', 
'BLVD':'BLVD', 
'CIR':'CIR', 
'CT':'CT', 
'DR':'DR', 
'FWY':'FWY', 
'LN':'LA', 
'PKWY':'PKWY', 
'PL':'PL', 
'PLAZA':'PLAZA', 
'RD':'RD',
'ST':'ST',
'STREET':'ST',
'STT':'ST',
'TER':'TR',
'WAY':'WAY'
}

all_properties = []
#instantiate encoder
encoder = geocoder()
count = 0
# Loop through the entries and get all of their data.
for key, line in enumerate(pdf_xml_texts):
    full_addr = line.text_content()
    addr_dict = {}
    lookup_addr = full_addr + " , Washington, DC"
    coords = encoder.geocode(lookup_addr)
    print coords
    print "Count: " + str(count)
    count += 1

    # TOSS OUT NON ADDRESSES BY SEEING IF THEY START WITH A NUMERIC CHARACTER
    if not full_addr[0].isdigit():
        continue

    # GET QUADRANT BEFORE SPLITTING
    if full_addr[-2:] in 'NW,NE,SW,SE' :
        addr_dict['street_quadrant'] = full_addr[-2:]
        rem_addr = full_addr[:-2].strip()
    else:
        addr_dict['street_quadrant'] = 'NW'
        rem_addr = full_addr.strip()

    # USE REMAINING PART
    
    # GET STREET NUMBER BY GETTING PART BEFORE FIRST SPACE    
    addr_dict['street_number'] = rem_addr[:rem_addr.find(' ')]

    # USE REMAINING PART
    rem_addr = rem_addr[rem_addr.find(' '):].strip()
    
    # GET STREET SUFFIX AND REST BY FINDING LAST SPACE. RISKY, BUT SEEMS TO WORK
    addr_dict['street_suffix'] = rem_addr[rem_addr.rfind(' ')+2:].upper().strip(' ,')
    addr_dict['street_suffix'] = suffix_strings[addr_dict['street_suffix']]

    addr_dict['street_name'] = rem_addr[:rem_addr.rfind(' ')].strip()
    addr_dict['addr_key'] = key
    addr_dict['coords'] = coords
    all_properties.append(addr_dict)
        

print all_properties

for prop in all_properties:
    scraperwiki.sqlite.save(['addr_key'], prop, table_name="dc_vacant_props", verbose=2)

go('https://www.taxpayerservicecenter.com/RP_Search.jsp?search_type=Assessment')
showforms()

def run_form():
    fv("1", "txtBuildingNumber", all_properties[0]['street_number'])
    fv("1", "txtStreetName", all_properties[0]['street_name'])
    fv("1", "txtThoroughfare", all_properties[0]['street_suffix'])
    fv("1", "txtQuadrant", all_properties[0]['street_quadrant'])

    submit()
    show()

run_form()

#showlinks()