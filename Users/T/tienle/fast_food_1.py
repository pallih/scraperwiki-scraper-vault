#Anthony Caratao, Tien Le, Matt Peterson, Michael Tuon
#5/31/13
#This scraper finds the appropriate information for each fast food chain from our webpage
import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders  
import string

us = geocoders.GeocoderDotUS() 
gn = geocoders.GeoNames()  

#html reference for the website to scrape
html = scraperwiki.scrape("http://www.delish.com/food-fun/fast-food-history#slide-1")
print html

root = lxml.html.fromstring(html)

mesa = ["div#slide1.slide.clearfix", "div#slide2.slide.clearfix", "div#slide3.slide.clearfix", "div#slide4.slide.clearfix", "div#slide5.slide.clearfix", "div#slide6.slide.clearfix", "div#slide7.slide.clearfix", "div#slide8.slide.clearfix", "div#slide9.slide.clearfix", "div#slide10.slide.clearfix", "div#slide11.slide.clearfix", "div#slide12.slide.clearfix"]

#nested for loop to extract various items from the webpage
for item in mesa:
    for div in root.cssselect("div#flipbookSlides"):
        
        rest = div.cssselect(item)[0]
        name = rest[1].cssselect("div.imageContentContainer")[0].cssselect("h2")[0].text
        open = rest[1].cssselect("div.imageContentContainer")[0].cssselect("div.imageContent")[0].cssselect("b")[0].tail
        loc = rest[1].cssselect("div.imageContentContainer")[0].cssselect("div.imageContent")[0].cssselect("b")[1].tail
        desc = rest[1].cssselect("div.imageContentContainer")[0].cssselect("div.imageContent")[0].cssselect("b")[2].tail
        
#adding data to the CSV file
        data = {
            'name': name,
            'open': open,
            'loc': loc,
            'desc': desc,
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)