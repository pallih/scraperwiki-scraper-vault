import scraperwiki

# Blank Python

import mechanize
import lxml.html
from array import *

url = "http://us.megabus.com/JourneyResults.aspx?originCode=138&destinationCode=123&outboundDepartureDate=6%2f13%2f2013&inboundDepartureDate=6%2f14%2f2013&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1"
br = mechanize.Browser()
br.set_handle_robots(False)
html = br.open(url).read()
x = 0
tree = lxml.html.fromstring(html)
for a in tree.cssselect('li[class=two]'):
    a[x] = a.text
    x = x + 1
for a in tree.cssselect('li[class=three] p'):
    print a.text
for a in tree.cssselect('li[class=five] p'):
    print a.textimport scraperwiki

# Blank Python

import mechanize
import lxml.html
from array import *

url = "http://us.megabus.com/JourneyResults.aspx?originCode=138&destinationCode=123&outboundDepartureDate=6%2f13%2f2013&inboundDepartureDate=6%2f14%2f2013&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1"
br = mechanize.Browser()
br.set_handle_robots(False)
html = br.open(url).read()
x = 0
tree = lxml.html.fromstring(html)
for a in tree.cssselect('li[class=two]'):
    a[x] = a.text
    x = x + 1
for a in tree.cssselect('li[class=three] p'):
    print a.text
for a in tree.cssselect('li[class=five] p'):
    print a.text