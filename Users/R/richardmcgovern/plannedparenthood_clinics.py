# Richard McGovern
# Date: 5/21/13
#
# DESCRIPTION: Geocodes addresses of Planned Parenthood Clinics in Washington State listed in this site:
#              http://www.plannedparenthood.org/health-center/findCenter.asp
#              Outputs a dbf table of the name and address of each clinic that may be downloaded on scraperwiki.

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

import mechanize
import cgi

us = geocoders.GeocoderDotUS()

# Create a browser object
import mechanize
br = mechanize.Browser()

# Open a webpage and inspect its contents
response = br.open('http://www.plannedparenthood.org/health-center/findCenter.asp')
print response.read()      # the text of the page
response1 = br.response()  # get the response again
print response1.read()     # can apply lxml.html.fromstring() NOT!

# List the forms that are in the page
for form in br.forms():
    print "Form name:", form.name
    print form

# Go to the state form and select "WA" for clinics in Washington state.
br.select_form(name="frmFindCenterRightInfo")
br['s'] = ["WA"]
resp = br.submit()

html = resp.get_data()

print html

################################

root = lxml.html.fromstring(html)

addressSection = root.cssselect("p.address")
print len(addressSection)


index = 0

failCount = 0
goodCount = 0
for p in addressSection:
    
    # Pass over the badly formatted address
    if not index == 7:
    
        # Get the name of the clinic.
        name = p.getparent().getparent().getparent().getchildren()[0].getchildren()[0].text_content()
        
        # Get the address.
        tags = p.getchildren()
        address = tags[0].text_content() + ' ' + tags[2].text_content() + tags[2].tail
        address += tags[3].text_content() + ' ' + tags[4].text_content()
        print address
    
        returned = us.geocode(address)
        if returned != None: 
            place, (lat, lng) = returned
            goodCount += 1

            data = {
                'name': name,
                'address': address,
                'lat': lat,
                'long': lng
            }
            scraperwiki.sqlite.save(unique_keys=['name'],data=data)
        else:

            # Default the geocoding to return that of Pike Place Market if it fails.
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
            place = "failed to geocode"
            print "failed to geocode"
            failCount += 1
    index += 1
print str(failCount) + " failed", str(goodCount) + " succeeded"

