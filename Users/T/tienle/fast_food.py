import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

#scrapes this site for the name of the restaurant, beginning of project.
html = scraperwiki.scrape("http://www.delish.com/food-fun/fast-food-history#slide-9")
print html
root = lxml.html.fromstring(html)
mesa = ["div#slide1.slide.clearfix", "div#slide2.slide.clearfix", "div#slide3.slide.clearfix", "div#slide4.slide.clearfix"]
for item in mesa:
    for div in root.cssselect("div#flipbookSlides"):
        rest = div.cssselect(item)[0]
        name = rest[1].cssselect("div.imageContentContainer")[0].cssselect("h2")[0].text
        data = {
            'name': name,    
        }
scraperwiki.sqlite.save(unique_keys=['name'],data=data)
import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

#scrapes this site for the name of the restaurant, beginning of project.
html = scraperwiki.scrape("http://www.delish.com/food-fun/fast-food-history#slide-9")
print html
root = lxml.html.fromstring(html)
mesa = ["div#slide1.slide.clearfix", "div#slide2.slide.clearfix", "div#slide3.slide.clearfix", "div#slide4.slide.clearfix"]
for item in mesa:
    for div in root.cssselect("div#flipbookSlides"):
        rest = div.cssselect(item)[0]
        name = rest[1].cssselect("div.imageContentContainer")[0].cssselect("h2")[0].text
        data = {
            'name': name,    
        }
scraperwiki.sqlite.save(unique_keys=['name'],data=data)
