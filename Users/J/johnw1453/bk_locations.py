#//////////////////////////////////////
#/John Williams
#/Geog 495 
#/May 2013
#/Wiki Scraper script
#/TA: Annie
#/Prof: Luke Bergmann
#//////////////////////////////////////


#////////////
#/used code from example scrapers and food truck scraper
#/worked for about 10 hours combined on the scraper
#/biggest road block was finding a website that would work
#/after that, various syntax errors and the fact that I am
#/not fluent in html posed other mediocre errors that consumed
#/a lot of time. overall i did what i could
#////////////




#//import the modules that will be used
#//for the script to get the html file,
#//parse it and then use geopy and geocoders
#//to geocode the addresses for use in the shapefile


import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string


#//bring in the two geocoders

us = geocoders.GeocoderDotUS()
gn = geocoders.GeoNames() 


#//'burgerkings' is what the html link was called and the scraperwiki scraped the website for the info
#//then the 'burgerkings' is printed which is the html scraped from the URL
#//then the lxml.html parses the html 

html = scraperwiki.scrape("http://www.mystore411.com/store/list_city/28/Washington/Seattle/Burger-King-store-locations")
print html

root = lxml.html.fromstring(html)


#//this for loop will go into the html and first go to 'tbody' and go through each 'tr'
#//then for each 'tr' that has exactly 3 'tds' the loop will collect data from the rows
#//'name' will be the text content of the first table row, 'address' will be the second
#//row and 'phone' will be taken from the third row. then the lists will be printed
data = []
for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        name = tds[0].text_content()
        address = tds[1].text_content()
        phone = tds[2].text_content()
        data = {
            'name' : name,
            'address' : address,
            'phone' : phone
        }

        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)


#//'street' is being set to the data value of 'address' since it is the
#//[1] row in the tr. this will pull it from the 'data' dictionary
#//'address' will be 'street' plus the string adding the city and state 
#//after it. then place will be lattitude and longitude to get a geocoded
#//address and then the print commmand will print the 'place', the latitude
#//and the longitude

        street = data.values()[2]

        address = street + ", Seattle, WA"

        print address

        returned = us.geocode(address)

        print type(returned)

        if returned != None:

#//use geocoder to print the address, latitude and longitude


            place, (lat, lng) = returned

        else:
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
            place = "failure to geocode"

        print "%s: %.5f, %.5f" % (place, lat, lng)

#//then a new data dictionary will be created with all the new
#//variables that were collected from geocoding
#
        data = {
            'name': name,
            'street address': address,
            'phone number': phone,
            'latitude coordinate': lat,
            'longitude coordinate': lng,
            'geocoder Result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)
#//////////////////////////////////////
#/John Williams
#/Geog 495 
#/May 2013
#/Wiki Scraper script
#/TA: Annie
#/Prof: Luke Bergmann
#//////////////////////////////////////


#////////////
#/used code from example scrapers and food truck scraper
#/worked for about 10 hours combined on the scraper
#/biggest road block was finding a website that would work
#/after that, various syntax errors and the fact that I am
#/not fluent in html posed other mediocre errors that consumed
#/a lot of time. overall i did what i could
#////////////




#//import the modules that will be used
#//for the script to get the html file,
#//parse it and then use geopy and geocoders
#//to geocode the addresses for use in the shapefile


import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string


#//bring in the two geocoders

us = geocoders.GeocoderDotUS()
gn = geocoders.GeoNames() 


#//'burgerkings' is what the html link was called and the scraperwiki scraped the website for the info
#//then the 'burgerkings' is printed which is the html scraped from the URL
#//then the lxml.html parses the html 

html = scraperwiki.scrape("http://www.mystore411.com/store/list_city/28/Washington/Seattle/Burger-King-store-locations")
print html

root = lxml.html.fromstring(html)


#//this for loop will go into the html and first go to 'tbody' and go through each 'tr'
#//then for each 'tr' that has exactly 3 'tds' the loop will collect data from the rows
#//'name' will be the text content of the first table row, 'address' will be the second
#//row and 'phone' will be taken from the third row. then the lists will be printed
data = []
for tr in root.cssselect("tbody tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        name = tds[0].text_content()
        address = tds[1].text_content()
        phone = tds[2].text_content()
        data = {
            'name' : name,
            'address' : address,
            'phone' : phone
        }

        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)


#//'street' is being set to the data value of 'address' since it is the
#//[1] row in the tr. this will pull it from the 'data' dictionary
#//'address' will be 'street' plus the string adding the city and state 
#//after it. then place will be lattitude and longitude to get a geocoded
#//address and then the print commmand will print the 'place', the latitude
#//and the longitude

        street = data.values()[2]

        address = street + ", Seattle, WA"

        print address

        returned = us.geocode(address)

        print type(returned)

        if returned != None:

#//use geocoder to print the address, latitude and longitude


            place, (lat, lng) = returned

        else:
            place, (lat, lng) = us.geocode("85 Pike St, Seattle, WA")
            place = "failure to geocode"

        print "%s: %.5f, %.5f" % (place, lat, lng)

#//then a new data dictionary will be created with all the new
#//variables that were collected from geocoding
#
        data = {
            'name': name,
            'street address': address,
            'phone number': phone,
            'latitude coordinate': lat,
            'longitude coordinate': lng,
            'geocoder Result': place
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)
