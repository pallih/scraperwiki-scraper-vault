import scraperwiki
import urllib
import lxml.html
import geopy
from geopy import geocoders
import string

html = scraperwiki.scrape("http://www.yellowpages.com/seattle-wa/guitar-stores")
print html

root = lxml.html.fromstring(html)

for div in root.cssselect("div.results"):

    sg = div.cssselect("div.search-content")
    storename = sg[0].cssselect("div.clearfix result track-listing vcard")[0].cssselect("div.listing-content")[0].cssselect("div.info")[0].cssselect("div.clearfix")[0].cssselect("h3")[0].cssselect("a")[0].text

    data = {
        'name': storename
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)

