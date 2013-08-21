import scraperwiki
from lxml.html import parse
import urllib2
import re
from geopy import geocoders

def getSynopID():
    url = 'http://www.meteorologic.net/archives-synop_07524.html'
    root = parse(urllib2.urlopen(url)).getroot()
    all_href = root.xpath("//div[@style='float:left;margin-right:25px;width:200px;']//a")
    for href in all_href:
        city = href.text_content().split("/")[0]
        url = href.attrib["href"]
        regExp = re.search('(?<=_)\w+', url)
        wmo = regExp.group(0)
#        print city, url, regExp.group(0)
        lat = lng = None
        try:
            lat, lng = getCoordinate(city)
        except TypeError:
            print "Oops!  city name %s is not valid " % city
            pass
        data = {"city" : city, "url" : url, "wmo" : wmo, "lat": lat, "lng": lng}
        scraperwiki.sqlite.save(unique_keys=["city"], data= data)

def getCoordinate(city):
    gn = geocoders.GeoNames()  
    place, (lat, lng) = gn.geocode(city+",FR",exactly_one=False)[0]
    return (lat,lng)


getSynopID()
    