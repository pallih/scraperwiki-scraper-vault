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

url = "http://www.kenmacdonaldproperties.co.uk/properties_srch.php"
def Main():
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    listingAddress = root.cssselect('p[style="font-weight:bold;text-align:right;margin:0px;margin-right:5px;"]')
    listingDescription = root.cssselect('p[style="font-weight:bold;text-align:right;margin:10px;"]')
    #listingStatus = root.cssselect('p[style="clear:both;font-weight:bold;color:crimson;text-align:right;margin:0px;margin-right:10px;margin-top:10px;"]')
    print "listingDescription: " + str(listingDescription)
    noOfListings = len(listingAddress)
    listingCounter = 0
    while listingCounter < noOfListings:
        data['Address'] = listingAddress[listingCounter].text_content()
        data['Description'] = listingDescription[listingCounter].text_content()
        #print "listingStatus: " + listingStatus[listingCounter].text_content() 
        listingCounter = listingCounter + 1
        #print "listingAddress: " + listingAddress[listingCounter].text_content()
        #print "listingDescription: " + listingDescription[listingCounter].text_content()

#        data['Status'] = listingStatus[listingCounter].text_content()
        scraperwiki.sqlite.save(unique_keys=['Date', 'Address', 'Description'], data=data)

Main()