# Geocode some factory lists
# Blank Python
import sys
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

# for the geocode
from geopy import geocoders

import json

pdfurl = "http://www.nikebiz.com/responsibility/documents/FactoryDisclosureList6.1.09.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

g = geocoders.Google('ABQIAAAAJWpc-texCflE7mMP0dgMGRTudD1_fegkcYIvU14JimqYoyT2khRxYTlCvIBPJApaoqvk4JfEfbrhyg')  

for page in root:
    assert page.tag == 'page'
    #print "page details", page.attrib
    pagelines = { }
    pagedata = { }
    for v in page:
        if v.tag == 'text':
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            top = int(v.attrib.get('top'))
            left = int(v.attrib.get('left'))

            if top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append(text)
            if left == 46: 
                pagedata[(top, 'country')] = text
            elif left < 150 and left > 46: 
                pagedata[(top, 'factory')] = text
            elif left > 200: 
                pagedata[(top, 'address')] = text
    lpagelines = pagelines.items()
    lpagelines.sort()
    blah = 0
    for top, line in lpagelines:
        blah = blah + 1
        line.sort()
        key = page.attrib.get('number') + ':' + str(top)
        
        try:
            factory = pagedata[(top, 'factory')]
            country = pagedata[(top, 'country')]
            address = pagedata[(top, 'address')]
            if address != '' and country != '': 
                place, (lat, lng) = g.geocode(address + " " + country)
                scraperwiki.datastore.save(unique_keys=[ 'key' ], data={ 'key' : key, 'factory': factory, 'country' : country, 'address': address,  'lat': lat, 'lng': lng })
        except Exception as e: 
            #print "error! ", e
            pass# Geocode some factory lists
# Blank Python
import sys
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

# for the geocode
from geopy import geocoders

import json

pdfurl = "http://www.nikebiz.com/responsibility/documents/FactoryDisclosureList6.1.09.pdf"

pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

g = geocoders.Google('ABQIAAAAJWpc-texCflE7mMP0dgMGRTudD1_fegkcYIvU14JimqYoyT2khRxYTlCvIBPJApaoqvk4JfEfbrhyg')  

for page in root:
    assert page.tag == 'page'
    #print "page details", page.attrib
    pagelines = { }
    pagedata = { }
    for v in page:
        if v.tag == 'text':
            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
            top = int(v.attrib.get('top'))
            left = int(v.attrib.get('left'))

            if top not in pagelines:
                pagelines[top] = [ ]
            pagelines[top].append(text)
            if left == 46: 
                pagedata[(top, 'country')] = text
            elif left < 150 and left > 46: 
                pagedata[(top, 'factory')] = text
            elif left > 200: 
                pagedata[(top, 'address')] = text
    lpagelines = pagelines.items()
    lpagelines.sort()
    blah = 0
    for top, line in lpagelines:
        blah = blah + 1
        line.sort()
        key = page.attrib.get('number') + ':' + str(top)
        
        try:
            factory = pagedata[(top, 'factory')]
            country = pagedata[(top, 'country')]
            address = pagedata[(top, 'address')]
            if address != '' and country != '': 
                place, (lat, lng) = g.geocode(address + " " + country)
                scraperwiki.datastore.save(unique_keys=[ 'key' ], data={ 'key' : key, 'factory': factory, 'country' : country, 'address': address,  'lat': lat, 'lng': lng })
        except Exception as e: 
            #print "error! ", e
            pass