import scraperwiki
from pyquery import PyQuery
import mechanize 

DOMAIN = 'http://en.wikipedia.org'
BASE_URL = "%s%s" % (DOMAIN, "/w/index.php?title=Special:WhatLinksHere/Template:OpenDomesday&namespace=0&limit=500")

br = mechanize.Browser()
br.addheaders = [('User-agent', 'ScraperWiki')]
br.set_handle_robots(False)
br.open(BASE_URL)
html = br.response().read()
pq = PyQuery(html)
print html

while True:
    links = pq("ul#mw-whatlinkshere-list li a:first")
    for link in links: 
        l = pq(link).attr('href')
        print l
