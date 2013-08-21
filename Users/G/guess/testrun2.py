###############################################################################
# Craigslist scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import json

#prep regex for money
money = re.compile('\$[0-9]+')

# LOOK FOR:
# <h4 class="ban">Sat Jul 23</h4>

rooturl = "http://newyork.craigslist.org/aap/index6300.html"
starturl = rooturl

soup = BeautifulSoup( scraperwiki.scrape( starturl ) )
#starturllink = soup.find(text=re.compile("next 100 postings"))
#starturl = rooturl + starturllink.parent['href']


#print soup.h4.nextSibling
#print "test"
#print soup.h4.nextSibling

print len(soup.findAll('h4'))
# print soup.findAll(attrs={"class":"ban"})

#print soup.prettify()
#print soup