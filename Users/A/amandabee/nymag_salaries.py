import scraperwiki
from bs4 import BeautifulSoup

import string
import urllib2
import urlparse
import re


html = scraperwiki.scrape("http://nymag.com/guides/salary/14497/index1.html")
soup = BeautifulSoup(html)

story = soup.find("div", id="story");

#for paragraph in story.find_all("p"):
    # print paragraph.contents
    # print paragraph.children



## How many pages are there? 
print soup.prettify()

for each in soup.find_all("li"):
    print each
import scraperwiki
from bs4 import BeautifulSoup

import string
import urllib2
import urlparse
import re


html = scraperwiki.scrape("http://nymag.com/guides/salary/14497/index1.html")
soup = BeautifulSoup(html)

story = soup.find("div", id="story");

#for paragraph in story.find_all("p"):
    # print paragraph.contents
    # print paragraph.children



## How many pages are there? 
print soup.prettify()

for each in soup.find_all("li"):
    print each
