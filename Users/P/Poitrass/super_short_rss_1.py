import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://rss.lapresse.ca/1011.xml',]

for i in range(len(sources)):       


    source = sources[i]

    html = scraperwiki.scrape(source)        #print html
    soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
    items = soup.findAll('item')             #print type(items) #print items[0]

    article = {}

    for item in items:
        article['title'] = item.find('title').text
        article['url'] = item.find('link').next # wow, this worked!
        article['ingress'] = item.find('description').text
        article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
        article['now'] = datetime.now()
        print article
        # the sensfull thing here would be to build a func to scrape the url form here.

        scraperwiki.sqlite.save(['title'], article)
