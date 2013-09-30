import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html
from lxml import etree
import BeautifulSoup
import HTMLParser
from datetime import date

data = {}
data['Date'] = date.today()

url = "http://www.western-isles-property.co.uk/common/script/property-listing.php?order=price&c=1"
def Main():
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    listingPrices = root.cssselect('a[class="listingprice"]')
    listingAddress = root.cssselect('a[class="listingaddress"]')
    listingDescription = root.cssselect('p[class="listingdescription"]')
    listingStatus = root.cssselect('span')
    noOfListings = len(listingPrices)
    listingCounter = 0
    print "data: " + str(data)
    while listingCounter < noOfListings:
        data['Price'] = listingPrices[listingCounter].text_content()
        data['Address'] = listingAddress[listingCounter].text_content()
        data['Description'] = listingDescription[listingCounter].text_content()
        #print "listingPrices: " + listingPrices[listingCounter].text_content()
        #print "listingAddress: " + listingAddress[listingCounter].text_content()
        #print "listingDescription: " + listingDescription[listingCounter].text_content()
        listingCounter = listingCounter + 1
        data['Status'] = listingStatus[listingCounter].text_content()
        scraperwiki.sqlite.save(unique_keys=['Date', 'Price', 'Address', 'Description','Status'], data=data)

Main()import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html
from lxml import etree
import BeautifulSoup
import HTMLParser
from datetime import date

data = {}
data['Date'] = date.today()

url = "http://www.western-isles-property.co.uk/common/script/property-listing.php?order=price&c=1"
def Main():
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    listingPrices = root.cssselect('a[class="listingprice"]')
    listingAddress = root.cssselect('a[class="listingaddress"]')
    listingDescription = root.cssselect('p[class="listingdescription"]')
    listingStatus = root.cssselect('span')
    noOfListings = len(listingPrices)
    listingCounter = 0
    print "data: " + str(data)
    while listingCounter < noOfListings:
        data['Price'] = listingPrices[listingCounter].text_content()
        data['Address'] = listingAddress[listingCounter].text_content()
        data['Description'] = listingDescription[listingCounter].text_content()
        #print "listingPrices: " + listingPrices[listingCounter].text_content()
        #print "listingAddress: " + listingAddress[listingCounter].text_content()
        #print "listingDescription: " + listingDescription[listingCounter].text_content()
        listingCounter = listingCounter + 1
        data['Status'] = listingStatus[listingCounter].text_content()
        scraperwiki.sqlite.save(unique_keys=['Date', 'Price', 'Address', 'Description','Status'], data=data)

Main()