import scraperwiki
import re
import urllib2
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

add = 'http://explore.georgetown.edu/faculty/index.cfm?Action=List&Letter=A&AffiliationID=210'
home = urlopen(add).read()
xmlSoup = BeautifulStoneSoup(home)

link = xmlSoup.findAll('a')
print len(link)
limit = len(link)
for link2 in link:
    print link2



