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
urlNews = 'http://www.wkow.com/search?vendor=ez&qu=middleton&searchtype=Text'
pageNews = mech.open(urlNews)
htmlNews = pageNews.read()
soupNews = BeautifulSoup(htmlNews, convertEntities=BeautifulSoup.HTML_ENTITIES)

resultsNews = soupNews.find('ol', {'class': 'wnGroup'})
itemNews = resultsNews.findAll('li')

for item in itemNews:
    prefixItem = 'http://www.wkow.com'
    headlineItem = item.find('span', {'class': 'text'}).text
    linkItem = prefixItem + item.a['href']
    summaryItem = item.find('p').text
    timeStamp = item.find('noscript').text
    timestampItem = parser.parse(timeStamp)
    
    articleNews = {
        'title': None,
        'link': None,
        'description': None,
        'pubDate': None,
    }
    
    articleNews['title'] = headlineItem
    articleNews['link'] = linkItem
    articleNews['description'] = summaryItem[:50]
    articleNews['pubDate'] = timestampItem
    
    print summaryItem
    scraperwiki.sqlite.save(["link"], articleNews)import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup, Tag
import urllib
import urllib2
import re
import types
import time, datetime
from dateutil import parser

mech = Browser()
urlNews = 'http://www.wkow.com/search?vendor=ez&qu=middleton&searchtype=Text'
pageNews = mech.open(urlNews)
htmlNews = pageNews.read()
soupNews = BeautifulSoup(htmlNews, convertEntities=BeautifulSoup.HTML_ENTITIES)

resultsNews = soupNews.find('ol', {'class': 'wnGroup'})
itemNews = resultsNews.findAll('li')

for item in itemNews:
    prefixItem = 'http://www.wkow.com'
    headlineItem = item.find('span', {'class': 'text'}).text
    linkItem = prefixItem + item.a['href']
    summaryItem = item.find('p').text
    timeStamp = item.find('noscript').text
    timestampItem = parser.parse(timeStamp)
    
    articleNews = {
        'title': None,
        'link': None,
        'description': None,
        'pubDate': None,
    }
    
    articleNews['title'] = headlineItem
    articleNews['link'] = linkItem
    articleNews['description'] = summaryItem[:50]
    articleNews['pubDate'] = timestampItem
    
    print summaryItem
    scraperwiki.sqlite.save(["link"], articleNews)