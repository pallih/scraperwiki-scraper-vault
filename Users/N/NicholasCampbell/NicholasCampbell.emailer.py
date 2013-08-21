# Nick Campbell
# Geog 495 Digital Geographies
# T.A. Annie Crane 
# Distilling the web into GIS datasets
#
# 
# 
# 


# Import  scaperwiki, lxml, and geocoding tools

import scraperwiki

import lxml.html

import geopy

from geopy import geocoders

import string



us = geocoders.GeocoderDotUS()

gn = geocoders.GeoNames()

# Establish the website that I am scraping

html = scraperwiki.scrape("http://www.mystore411.com/store/list_city/15/Washington/Kirkland/Starbucks-store-locations")


# Print html 

print html

# Retrieve HTML from website

root = lxml.html.fromstring(html)

# Select the data from my tables. My name, address and phone data for Starbucks in Kirkland, WA

for tr in root.cssselect("tbody tr"):

    tds = tr.cssselect("td")
    if len(tds)==3:
        Name = tds[0].text_content()
        Address = tds[1].text_content()
        Phone = tds[2].text_content()
        data = {
            'Name' : Name,
            'Address' : Address,
            'Phone' : Phone
        }

# Print list of name, adress and phone data from website


        print data

# Establish the addresses that I will be operating on. When I printed my data, for some reason 'Address' printed third instead of second so I wrote [2} so the third data set is operated on.

        street = data.values()[2]

# Add Kirkland, WA to each address so they can be better matached

        address = street + ", Kirkland, WA"

        print address


        returned = us.geocode(address)
        
        print type(returned)

#Specify an arbitrary address for addresses that failed to geocode. I chose the default address because I did not want this address to be in Kirkland.
        
        if returned != None:
        
            place, (lat, lng) = returned

        else:
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
            place = "FAILED TO GEOCODE"

#Use the geocoder to print the address, latitude coordinates and longitude coordinate

        
        print "%s: %.5f, %.5f" % (address, lat, lng)

#Establish the list of data categories I would like to include in my exported table.


        data = {
            'name': Name,
            'Street Address': Address,
            'Phone Number': Phone,
            'Latitude Coordinate': lat,
            'Longitude Coordinate': lng,
            'Geocoder Result': place
        }

#Create table

        scraperwiki.sqlite.save(unique_keys=['name'],data=data)

    
      
        


