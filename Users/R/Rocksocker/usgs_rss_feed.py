import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re



def strip_tags(html):
    return ' '.join(html.findAll(text=True))

source = "http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M7.xml"

html = scraperwiki.scrape(source)        #print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
items = soup.findAll('item')             #print type(items) #print items[0]

article = {}


for item in items:
    article['title']         = item.find('title').text
    article['description']   = item.find('description').text
    article['url']           = item.find('link').next # wow, this worked!
    article['pubdate']       = dateutil.parser.parse(item.find('pubdate').text)
    article['lat']           = item.find('geo:lat').text
    article['long']          = item.find('geo:long').text
    article['magnitude']     = item.find('dc:subject').text
    
    print article
    # the sensfull thing here would be to build a func to scrape the url form here.

    scraperwiki.sqlite.save(['title'], article)
import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re



def strip_tags(html):
    return ' '.join(html.findAll(text=True))

source = "http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M7.xml"

html = scraperwiki.scrape(source)        #print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
items = soup.findAll('item')             #print type(items) #print items[0]

article = {}


for item in items:
    article['title']         = item.find('title').text
    article['description']   = item.find('description').text
    article['url']           = item.find('link').next # wow, this worked!
    article['pubdate']       = dateutil.parser.parse(item.find('pubdate').text)
    article['lat']           = item.find('geo:lat').text
    article['long']          = item.find('geo:long').text
    article['magnitude']     = item.find('dc:subject').text
    
    print article
    # the sensfull thing here would be to build a func to scrape the url form here.

    scraperwiki.sqlite.save(['title'], article)
