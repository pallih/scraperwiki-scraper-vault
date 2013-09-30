#Welcome to Matt Peterson's feeble attempt at writing a WikiScraper code, which somehow ends up working.  
#Time to import a bunch of awesome modules.  

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders
import string
import re

#Now we need the geocoders.  

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

#Now it's time to set our url to scrape.  
#I've found a website that lists some of the top Seafood restaurants in the Seattle area.  
#I love seafood, so let's go to work.

html = scraperwiki.scrape("http://www.zagat.com/seattle/seafood-restaurants")
print html

root = lxml.html.fromstring(html)

#First we need to find the section of source code that contains the entire table.  

mytable = root.cssselect("div#records.seo-friendly")[0]

#Next, it's time to put our cursor to the level of html that contains all the information we need and is repeated throughout the page.  

for sf in mytable.cssselect("div.primary"):

#sf stands for seafood.
#Inside the first seafood, the name of the restaurant is inside h3 and a.
#Address is in the third seafood inside h4, and citystate is the next line below.  

    name = sf[0].cssselect("h3")[0].cssselect("a")[0].text
    address = sf[2].cssselect("h4")[0].text
    citystate = sf[2].cssselect("h4")[0].cssselect("br")[0].tail

#Because the addresses in the website all include parenthetical locational references (between 3rd and 4th Street, for example), we need to get rid of that content so it doesn't confuse the geocoder.    

    regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
    m = regEx.match(address)
    while m:
        address = m.group(1) + m.group(2)
        m = regEx.match(address)
    print address

#Now it's time to geocode these points.  
#In case the geocoder is still confused, we throw in an exception that results in "failed to geocode".  

    returned = us.geocode(address + citystate)
    if returned != None: 
        place, (lat, lng) = returned
    else:
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
#Now it's time to outline the data that the scraper will produce.  

    data = {
        'name': name,
        'address': address,
        'citystate': citystate,
        'lat': lat,
        'long': lng,
        'place': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)

#And the code works!!!
#All of the records from the first page of our website are scraped.  
#I attempted to scrape the other five pages as well, using a for loop, but it proved too complicated and I couldn't get it to work.  
#This was collaborated with Anthony Caratao, whose successful code provided sufficient reference between his and Luke's to make mine work.  
#Also, Luke provided a couple of very helpful hints.  
#This code was based off of Luke's code, but the regEx segment was found on a Python forum.  
#I cycled through three or four different websites, writing code that ran successfully but scraped no data on at least two websites. 
#This assignment took approximately twelve hours to complete.  #Welcome to Matt Peterson's feeble attempt at writing a WikiScraper code, which somehow ends up working.  
#Time to import a bunch of awesome modules.  

import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders
import string
import re

#Now we need the geocoders.  

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

#Now it's time to set our url to scrape.  
#I've found a website that lists some of the top Seafood restaurants in the Seattle area.  
#I love seafood, so let's go to work.

html = scraperwiki.scrape("http://www.zagat.com/seattle/seafood-restaurants")
print html

root = lxml.html.fromstring(html)

#First we need to find the section of source code that contains the entire table.  

mytable = root.cssselect("div#records.seo-friendly")[0]

#Next, it's time to put our cursor to the level of html that contains all the information we need and is repeated throughout the page.  

for sf in mytable.cssselect("div.primary"):

#sf stands for seafood.
#Inside the first seafood, the name of the restaurant is inside h3 and a.
#Address is in the third seafood inside h4, and citystate is the next line below.  

    name = sf[0].cssselect("h3")[0].cssselect("a")[0].text
    address = sf[2].cssselect("h4")[0].text
    citystate = sf[2].cssselect("h4")[0].cssselect("br")[0].tail

#Because the addresses in the website all include parenthetical locational references (between 3rd and 4th Street, for example), we need to get rid of that content so it doesn't confuse the geocoder.    

    regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
    m = regEx.match(address)
    while m:
        address = m.group(1) + m.group(2)
        m = regEx.match(address)
    print address

#Now it's time to geocode these points.  
#In case the geocoder is still confused, we throw in an exception that results in "failed to geocode".  

    returned = us.geocode(address + citystate)
    if returned != None: 
        place, (lat, lng) = returned
    else:
        place = "FAILED TO GEOCODE" 
    print "%s: %.5f, %.5f" % (place, lat, lng)  
    
#Now it's time to outline the data that the scraper will produce.  

    data = {
        'name': name,
        'address': address,
        'citystate': citystate,
        'lat': lat,
        'long': lng,
        'place': place
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)

#And the code works!!!
#All of the records from the first page of our website are scraped.  
#I attempted to scrape the other five pages as well, using a for loop, but it proved too complicated and I couldn't get it to work.  
#This was collaborated with Anthony Caratao, whose successful code provided sufficient reference between his and Luke's to make mine work.  
#Also, Luke provided a couple of very helpful hints.  
#This code was based off of Luke's code, but the regEx segment was found on a Python forum.  
#I cycled through three or four different websites, writing code that ran successfully but scraped no data on at least two websites. 
#This assignment took approximately twelve hours to complete.  