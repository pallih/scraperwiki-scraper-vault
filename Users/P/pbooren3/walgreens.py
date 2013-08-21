#Peter Booren
#GEOG 495 TA ANNIE
#SECOND ATTEMPT AT "Distilling the web into GIS datasets" lab

#Spent about 5 hours this round (with success, 2 hrs last time)
#decided to use a different web page, this was much easier to use!



#import all of the tools I will need and the geocoder
import scraperwiki

import lxml.html

import geopy

from geopy import geocoders

import string

#Geocoder borrowed from Bergmann's food truck script

us = geocoders.GeocoderDotUS()

gn = geocoders.GeoNames()


#Easy website I found from google when I searched for 'Walgreens in Seattle' 8th hit or so, Nick suggested this "411" site is very easy to negotiate with
#decided on walgreens b/c I worked with them in an internship in the past... no specific reason otherwise
 
html = scraperwiki.scrape ("http://www.mystore411.com/store/list_city/21/Washington/Seattle/Walgreens-store-locations")

print html

# set the root and parse out what I need from the source code


root = lxml.html.fromstring(html)

for tr in root.cssselect("tbody tr"):

    tds = tr.cssselect("td")
    if len (tds)==3:
        Name = tds[0].text_content()
        Address = tds[1].text_content()
        Phone = tds[2].text_content()
       

# Separated everything that I needed from the source code into three different categories I will be working with, Name of store, Address, and Phone number

       
# begin the geocoding process, add Seattle, WA to the end of each address for increased accuracy
        street = Address
        address1 = street + ", Seattle, WA"

        print address1
        
        returned = us.geocode (address1)


# set conditional statement for when the geocoder doesnt return a result. I decided to use my house as the default address, a fun and easy way to recognize an error
        print type(returned)
        if returned != None:
            place, (lat, lng) = returned

        else:
            place, (lat, lng) = us.geocode("1310 Ne 52nd St, Seattle, WA")
            place = "FAILED TO GEOCODE"

        print "%s: %.5f, %.5f" % (address1, lat, lng)

#extract and save the data that will be used to create my table


        data = {
            'Name' : Name,
            'Street Address' :address1,
            'Address' : street,
            'Phone' : Phone,
            'Latitude' : lat,
            'Longitude': lng
            }
        print data  
        scraperwiki.sqlite.save(['Name'], data=data)

#Output is a table that has all of the categories above with a spatial value 
#Output.csv file will be converted into lyr file then to a shapefile for use with arcgis within the python module, script uploaded seperately!




