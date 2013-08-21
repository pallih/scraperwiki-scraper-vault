# Blank Python
from lxml import etree

import lxml.html
import scraperwiki
import xmltodict
scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
xml = scraperwiki.scrape('http://grapevine.is/modules/rss/rss.aspx?category=News')

start = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>grapevine.is</title><link>http://grapevine.is</link><description>Grapevine daily rss</description>\n'

doc = xmltodict.parse(xml)
for x in doc['rss']['channel']['item'][:5]:
        start = start +'<item>'
        start = start +'<title>'+ x['title'] + '</title>\n'
        start = start +'<link>'+ x['link'] + '</link>\n'
        start = start +'<pubDate>'+ x['pubdate'] + '</pubDate>\n'
        start = start +'<description>'+ x['description'] + '</description>\n'
        html = scraperwiki.scrape(x['link'])
        root2 = lxml.html.fromstring(html)
        img_link = root2.xpath('//div[@id="image_big"]/img')
        start = start +'<enclosure url="http://grapevine.is'+ img_link[0].attrib['src'] + '" length="12216320" type="image/jpeg"/>\n'

    #print img_link[0].attrib['src']

        start = start +'</item>\n'
start = start + '</channel></rss>'
print start# Blank Python
from lxml import etree

import lxml.html
import scraperwiki
import xmltodict
scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
xml = scraperwiki.scrape('http://grapevine.is/modules/rss/rss.aspx?category=News')

start = '<?xml version="1.0" encoding="utf-8"?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel><title>grapevine.is</title><link>http://grapevine.is</link><description>Grapevine daily rss</description>\n'

doc = xmltodict.parse(xml)
for x in doc['rss']['channel']['item'][:5]:
        start = start +'<item>'
        start = start +'<title>'+ x['title'] + '</title>\n'
        start = start +'<link>'+ x['link'] + '</link>\n'
        start = start +'<pubDate>'+ x['pubdate'] + '</pubDate>\n'
        start = start +'<description>'+ x['description'] + '</description>\n'
        html = scraperwiki.scrape(x['link'])
        root2 = lxml.html.fromstring(html)
        img_link = root2.xpath('//div[@id="image_big"]/img')
        start = start +'<enclosure url="http://grapevine.is'+ img_link[0].attrib['src'] + '" length="12216320" type="image/jpeg"/>\n'

    #print img_link[0].attrib['src']

        start = start +'</item>\n'
start = start + '</channel></rss>'
print start