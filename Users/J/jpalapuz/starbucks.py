## Lists Starbucks locations in Seattle, WA

import scraperwiki
import lxml.html 
import urllib
import string
import geopy
from geopy import geocoders

us = geocoders.GeocoderDotUS()

html = scraperwiki.scrape("http://www.mystore411.com/store/list_city/15/Washington/Seattle/Starbucks-store-locations")
root = lxml.html.fromstring(html)

## Goes over the first part of the table and stores information for each Starbucks address
## Table is divided into two since the middle of the table includes 'tr' for an advertisement.
for tr in root.cssselect("table[class='table1'] tr")[2:26]:

    tds = tr.cssselect("td")

    name = tds[0].cssselect("a")[0].text   ## Gets the name of the Starbucks store
    address = tds[1].text                  ## Gets the address of the store
    city_state = "Seattle, WA"             ## A string to include the city and state, used for geocoding
    phone = tds[2].text                    ## Gets the phone number of the store

    ## The following geocodes the address of the store to get it's x,y coordinates.
    ## If location is not found, it prints an error message".
    location = us.geocode(address + ", " + city_state)
    if location != None: 
        place, (lat, lng) = location
    else:
        place = "Cannot be located." 
    
    ## Stores data in ScraperWiki 
    data = {
        'Name' : name,
        'Address' : address,
        'Phone' : phone,
        'Latitude' : lat,
        'Longitude' : lng
    }

## Goes over the second part of the table and stores information.
for tr in root.cssselect("table[class='table1'] tr")[28:]:

    tds = tr.cssselect("td")

    name = tds[0].cssselect("a")[0].text   ## Gets the name of the Starbucks store
    address = tds[1].text                  ## Gets the address of the store
    city_state = "Seattle, WA"             ## A string to include the city and state, used for geocoding
    phone = tds[2].text                    ## Gets the phone number of the store

    ## The following geocodes the address of the store to get it's x,y coordinates.
    ## If location is not found, it prints an error message".
    location = us.geocode(address + ", " + city_state)
    if location != None: 
        place, (lat, lng) = location
    else:
        place = "Cannot be located." 
    

    
    ## Stores data in ScraperWiki
    data = {
        'Name' : name,
        'Address' : address,
        'Phone' : phone,
        'Latitude' : lat,
        'Longitude' : lng
    }
    
    scraperwiki.sqlite.save(unique_keys=['Address'], data=data)
    
