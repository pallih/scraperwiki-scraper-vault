import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
import dateutil.parser
import re


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

source = "http://mopac.peopleadmin.com/rss/258.xml"

html = scraperwiki.scrape(source)        #print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
items = soup.findAll('item')             #print type(items) #print items[0]

article = {}

for item in items:
    if re.search('it manager', item.find('title').text, re.IGNORECASE):
        article['title']         = item.find('title').text
        article['link']          = item.find('link').text
        article['desc']          = item.find('description').text
        article['author']        = item.find('author').text
        article['guid']          = item.find('guid').text
        article['pubdate']       = dateutil.parser.parse(item.find('pubdate').text)
        article['source']        = item.find('source').text

        scraperwiki.sqlite.save(['title'], article)
    import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
import dateutil.parser
import re


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

source = "http://mopac.peopleadmin.com/rss/258.xml"

html = scraperwiki.scrape(source)        #print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
items = soup.findAll('item')             #print type(items) #print items[0]

article = {}

for item in items:
    if re.search('it manager', item.find('title').text, re.IGNORECASE):
        article['title']         = item.find('title').text
        article['link']          = item.find('link').text
        article['desc']          = item.find('description').text
        article['author']        = item.find('author').text
        article['guid']          = item.find('guid').text
        article['pubdate']       = dateutil.parser.parse(item.find('pubdate').text)
        article['source']        = item.find('source').text

        scraperwiki.sqlite.save(['title'], article)
    