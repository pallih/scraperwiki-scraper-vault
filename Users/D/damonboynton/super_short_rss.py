import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://www.amazon.es/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.ca/gp/rss/new-releases/dvd/917972/ref=zg_bsnr_917972_rsslink',
            'http://www.amazon.fr/gp/rss/new-releases/dvd/405322/ref=zg_bsnr_405322_rsslink',
            'http://www.amazon.co.uk/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.it/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.co.jp/gp/rss/new-releases/dvd/562016/ref=zg_bsnr_562016_rsslink']

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
import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://www.amazon.es/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.ca/gp/rss/new-releases/dvd/917972/ref=zg_bsnr_917972_rsslink',
            'http://www.amazon.fr/gp/rss/new-releases/dvd/405322/ref=zg_bsnr_405322_rsslink',
            'http://www.amazon.co.uk/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.it/gp/rss/new-releases/dvd/ref=zg_bsnr_dvd_rsslink',
            'http://www.amazon.co.jp/gp/rss/new-releases/dvd/562016/ref=zg_bsnr_562016_rsslink']

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
