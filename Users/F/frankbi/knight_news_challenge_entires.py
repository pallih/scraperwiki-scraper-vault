import scraperwiki
import lxml
import requests
import re

from lxml import html

baseUrl='http://newschallenge.tumblr.com/page/'
for i in range(1, 66):
    fullurl= baseUrl + str(i)
    print 'Scraping url ', fullurl
    r=requests.get(fullurl)
    root = lxml.html.fromstring(r.content)
    for entry in root.cssselect('div.postbox'):
        try:
            h2 = entry.cssselect('h2')[0]
        except IndexError:
            print 'Index error caught', url, entry
        title = h2.text_content().strip()
        try:
            href = h2.cssselect('a')[0]
        except IndexError:
            print 'Index error caught', url, entry
        try:
            url = h2.xpath('a/@href')[0]
        except IndexError:
            print 'Index error caught', url, entry
        scraperwiki.sqlite.save(unique_keys=["url"], data={"title":title, "url":url})