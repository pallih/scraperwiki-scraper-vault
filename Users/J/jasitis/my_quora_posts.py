import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
# test for å se hva jeg kan få ut av en rss.

def strip_tags(html):
    return ' '.join(html.findAll(text=True))

source = "http://feeds.feedburner.com/pinterest/EiMe"

html = scraperwiki.scrape(source)        #print html
soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
items = soup.findAll('item')             #print type(items) #print items[0]

article = {}

for item in items:
    article['title'] = item.find('title').text
    article['url'] = item.find('link').next # wow, this worked!
    article['ingress'] = item.find('description').text
    # there is also an image, but I dont think I need that
    article['now'] = datetime.now()
    print article
    # the sensfull thing here would be to build a func to scrape the url form here.

    scraperwiki.sqlite.save(['title'], article)
