# Richard McGovern
# Geog 495 Bergmann
# May 8, 2013
#
# DESCRIPTION: US geocoder cannot interpret any of these addresses
#

import string
import scraperwiki
from geopy import geocoders
us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("https://www.seattle.gov/neighborhoods/ppatch/locations.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)

######
def gc(dict_values):
    #print dict_values
    print type(dict_values)
    address = dict_values
    #loc =  address + ", Seattle, WA"
    loc = "1308 5th Avenue, Seattle, Washington"
    #filtered_address = " ".join(loc.split('&'))
    filtered_address = filter(lambda c: c in string.digits + ',' + '&' + '.' + ' ' + "#" + string.letters, loc)
    print filtered_address
    returned = us.geocode(filtered_address)
    
    if returned != None:
        place, (lat, lng) = returned
    else:
        place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
        place = "FAILED TO GEOCODE"
    
    coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
    coords = coordinates.split(":")
    lat_long = coords[1]

    #if loc != None:
        
     #   place, (lat, lng) = us.geocode(loc)

     #   coordinates = "%s: %.5f, %.5f" % (place, lat, lng)
     #   split = coordinates.split(":")

    #    lat_long = split[1]
    #else:
    #    lat_long = "Failed to geocode latitude, Failed to geocode longitude"
    return lat_long
######



# Table containing P Patch names and addresses.
PPatchLocs = root.cssselect("table table")

PPNamesList = []

# Make list of addresses.
addrSpanList = PPatchLocs[2].cssselect("span.style3")
addrList = []
index = 0


## DOES span.style3 => a link tag exists for this PPatch? NO! Greenwood station
## Need to check if there is a link tag there first

badIndices = []
for span in addrSpanList:
    if not "(" in span.text:
        addrList.append(span.text)
    else:
        badIndices.append(index)
    index += 1

# Make list of P Patch names.
x = 0
for link in PPatchLocs[2].cssselect("a"):
    if not x in badIndices:
        PPNamesList.append(link.text)
    x += 1

# Print "<ppatch name> <address>"
i = 0
for pp in PPNamesList:

    data = {
        'ppatchName' : pp,
        'address' : addrList[i]
    }
    scraperwiki.sqlite.save(unique_keys=['ppatchName'], data=data)
    i += 1
    print gc(data.values()[1])

#loc = address + ", "
#us.geocode



print len(PPNamesList), len(addrList) # 73 77 WTF??? Addresses are not matching up
