import scraperwiki

#import GeoIP
#gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
#print gi.country_name_by_addr("212.13.195.240")


#!/usr/bin/python
import urllib2
from pyquery import PyQuery as pq
from lxml import etree
import urllib

mime_type = 'application/xml'
user_agent = 'ScraperWiki'
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0) Gecko/20100101 Firefox/6.0'
data = None 
headers = dict({
    'Accept': mime_type, 
    'User-Agent': user_agent
})
req = urllib2.Request('http://en.wikipedia.org/wiki/Southern_Cassowary', data, headers)
content = urllib2.urlopen(req)
html = content.read()
#print html


#d = pq("<html></html>")
#d = pq(etree.fromstring(html))
import lxml.html
d = pq(lxml.html.fromstring(html))
#d = pq(url='http://google.com/')
#d = pq(url='http://google.com/', opener=lambda url: urllib.urlopen(url).read())
#d = pq(filename=path_to_html_file)

print d('.infobox')

try:
    html = scraperwiki.scrape("http://en.wikipedia.org/wiki/Southern_Cassowary")
    print html
except urllib2.HTTPError, e:
    print e


#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data

#scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki

#import GeoIP
#gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
#print gi.country_name_by_addr("212.13.195.240")


#!/usr/bin/python
import urllib2
from pyquery import PyQuery as pq
from lxml import etree
import urllib

mime_type = 'application/xml'
user_agent = 'ScraperWiki'
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0) Gecko/20100101 Firefox/6.0'
data = None 
headers = dict({
    'Accept': mime_type, 
    'User-Agent': user_agent
})
req = urllib2.Request('http://en.wikipedia.org/wiki/Southern_Cassowary', data, headers)
content = urllib2.urlopen(req)
html = content.read()
#print html


#d = pq("<html></html>")
#d = pq(etree.fromstring(html))
import lxml.html
d = pq(lxml.html.fromstring(html))
#d = pq(url='http://google.com/')
#d = pq(url='http://google.com/', opener=lambda url: urllib.urlopen(url).read())
#d = pq(filename=path_to_html_file)

print d('.infobox')

try:
    html = scraperwiki.scrape("http://en.wikipedia.org/wiki/Southern_Cassowary")
    print html
except urllib2.HTTPError, e:
    print e


#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr.tcont"):
#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data

#scraperwiki.sqlite.save(unique_keys=['country'], data=data)
