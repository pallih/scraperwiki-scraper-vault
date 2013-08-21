import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup, Tag
import urllib
import urllib2
import re
import types
import time, datetime
from dateutil import parser

mech = Browser()
urlScrape = 'http://www.cityofmadison.com/transportation/roadworks/'
pageScrape = mech.open(urlScrape)
htmlScrape = pageScrape.read()
soupScrape = BeautifulSoup(htmlScrape, convertEntities=BeautifulSoup.HTML_ENTITIES)
resultsScrape = soupScrape.find('div', {'class': 'link_list'})
itemScraped = resultsScrape.findAll('li')

for item in itemScraped:
    prefixItem = 'http://www.cityofmadison.com'
    infoLink = prefixItem + item.a['href']
    infoTitle = item.findAll('strong')
    infoText = item.findAll('span')
    
    itemLink = infoLink
    itemTitle = infoTitle[0].text
    itemDate = infoText[0].text
    itemLocation = infoText[1].text

    print 'Road Project: %s. Date of project: %s. Location of project: %s. Read More: %s' % (itemTitle, itemDate, itemLocation, itemLink)