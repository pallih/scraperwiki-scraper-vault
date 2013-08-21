import lxml.html
from lxml import etree
import scraperwiki
import urllib, urlparse
from dateutil import parser

url = "http://www.blumar.com/noticias.html"
root = lxml.html.fromstring(scraperwiki.scrape(url))
news = {}

for box in root.cssselect('div.box_nota'):
    par = box.cssselect('p')[0]
    news['date'] = parser.parse(par.cssselect('span')[0].text)
    news['title'] = par.cssselect('span')[1].text
    news['link'] = 'http://blumar.com' + box.cssselect('p')[2].cssselect('span')[0].cssselect('a')[0].attrib['href']
    news['summary'] = box.cssselect('p')[1].text_content()
    scraperwiki.sqlite.save(['link'], news)





