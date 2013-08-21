import scraperwiki       
import urllib
import lxml.html
import geopy
from geopy import geocoders
import string

us = geocoders.GeocoderDotUS()
gn = geocoders.GeoNames()

html = scraperwiki.scrape("http://webdesign.about.com/od/pricing/l/bl_median_salaries_web_designer.htm")


root = lxml.html.fromstring(html)

CITY = ''
STATE = ''
for tr in root.cssselect("div div#articlebody tr"):
        
    tds = tr.cssselect("td")
    
    #State / city
    location: tds[0].text_content()
    
    #Salary per year
    salary : tds[1].text_content()

    #location in coordinates
    
    
    #http://www.geonames.org/search.html?q=seattle%2C+wa&country=

    data = {
            'location' : location,
            'annual salary' : salary
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['location'], data=data)

