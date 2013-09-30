# Metacritic game publications

import scraperwiki
import lxml.html
import re
import httplib
import urllib2

#Check if URL exists
def url_exists(location):
    request = urllib2.Request(location)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False

#Go through the pages
for i in range(0,4):
    url = "http://www.metacritic.com/browse/games/publication/reviewed?num_items=100&page="+str(i)
    if(url_exists(url)):
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        
        publications = root.xpath("//ol[@class='list_products list_entities']/li")
        
        for publication in publications:
            data = {}
            data['name'] = str(publication.xpath("div/div/div/h3/a/text()")[0])
        
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)# Metacritic game publications

import scraperwiki
import lxml.html
import re
import httplib
import urllib2

#Check if URL exists
def url_exists(location):
    request = urllib2.Request(location)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except urllib2.HTTPError:
        return False

#Go through the pages
for i in range(0,4):
    url = "http://www.metacritic.com/browse/games/publication/reviewed?num_items=100&page="+str(i)
    if(url_exists(url)):
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        
        publications = root.xpath("//ol[@class='list_products list_entities']/li")
        
        for publication in publications:
            data = {}
            data['name'] = str(publication.xpath("div/div/div/h3/a/text()")[0])
        
            scraperwiki.sqlite.save(unique_keys=['name'], data=data)