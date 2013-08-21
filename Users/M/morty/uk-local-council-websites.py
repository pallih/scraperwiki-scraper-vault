import scraperwiki
from lxml import etree
from urllib import quote
import json
from urlparse import urlparse

url = "http://tagish.co.uk/links/localgov.htm"

def mentions_iar(url):
    search_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&key=ABQIAAAAzESE3t9QhAz69GaZMQasqhQWj4N4t6Xmv-CV_W48hf2y5mqxJRTHd2g0xS2z9S2AR_LF7jz4xq_w5Q&q=' + quote('"information asset register" inurl:%s' % urlparse(url).netloc)
    result = json.loads(scraperwiki.scrape(search_url))
    data = result['responseData']
    return len(data['results']) 

html = scraperwiki.scrape(url)
doc = etree.HTML(html)

for l in doc.xpath('//ul/li/a'):
    if l.attrib['href'] == 'Agencies_By_Department.htm':
        break
    scraperwiki.sqlite.save(['council_name'], {'council_name': l.text, 'url': l.attrib['href'], 'mentions_of_iar': mentions_iar(l.attrib['href'])})
