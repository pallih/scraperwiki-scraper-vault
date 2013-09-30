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

url = "http://www.hebea.co.uk/property-list.php?order=price"
def Main():
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    listings = root.cssselect('div[id="listing"] table[class="listingtable"] tr')
    #dictionary = scraperwiki.sqlite.select("* from 'swdata'")
    #print len(dictionary)
    property_links = root.xpath("//div[@class='listingimage']/a/@href")
    print property_links
    for listing in listings:
        tds = listing.cssselect('td')
        
        data['Price'] = tds[0].text_content()
        divs = tds[1].cssselect('div')
        data['Address'] = divs[0].text_content()
        data['Description'] = divs[1].text_content()
        data['Status'] = tds[2].text_content()
        #scraperwiki.sqlite.save(unique_keys=['Date', 'Price', 'Address', 'Description', 'Status'], data=data)
#        for td in tds:
#            print td.text_content()

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

url = "http://www.hebea.co.uk/property-list.php?order=price"
def Main():
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    listings = root.cssselect('div[id="listing"] table[class="listingtable"] tr')
    #dictionary = scraperwiki.sqlite.select("* from 'swdata'")
    #print len(dictionary)
    property_links = root.xpath("//div[@class='listingimage']/a/@href")
    print property_links
    for listing in listings:
        tds = listing.cssselect('td')
        
        data['Price'] = tds[0].text_content()
        divs = tds[1].cssselect('div')
        data['Address'] = divs[0].text_content()
        data['Description'] = divs[1].text_content()
        data['Status'] = tds[2].text_content()
        #scraperwiki.sqlite.save(unique_keys=['Date', 'Price', 'Address', 'Description', 'Status'], data=data)
#        for td in tds:
#            print td.text_content()

Main()