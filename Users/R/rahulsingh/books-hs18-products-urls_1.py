import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import urllib2
import re

scraperwiki.sqlite.attach('books-hs18-pages-results','url')
list_urls = scraperwiki.sqlite.select('* from url.swdata')
print 'length :'+str(len(list_urls))
print type(list_urls)

count=0
print type(count)
for urls in list_urls:
  url_category = urls.values()
  url = url_category[0]
  category = url_category[1]
  print 'loop : '+url
  count = count+1
  print count
  http = httplib2.Http()
  status, response = http.request(url)

  links = []

  for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
      #print 'inside if of href'
      url = link['href']
      #match = re.search(r'http://www.homeshop18.com/[\w\s\d-]+/author:[\w\d-]+/isbn:\d+/books/'+category4url+'/product:\d+/cid:\d+/',str(link))
      match = re.search(r'http://www.homeshop18.com/[\w\s\d-]+/author:[\w\d-]+/isbn:\d+/books/[\w\d-]+/product:\d+/cid:\d+/',str(link))
      if match:
        url = url.replace("</a>","")
        print match.group()
        links.append(url)
          
        scraperwiki.sqlite.save(["url","category"],{'url':url,'category':category},"swdata")
          
print len(links)
print type(links)


  
import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import urllib2
import re

scraperwiki.sqlite.attach('books-hs18-pages-results','url')
list_urls = scraperwiki.sqlite.select('* from url.swdata')
print 'length :'+str(len(list_urls))
print type(list_urls)

count=0
print type(count)
for urls in list_urls:
  url_category = urls.values()
  url = url_category[0]
  category = url_category[1]
  print 'loop : '+url
  count = count+1
  print count
  http = httplib2.Http()
  status, response = http.request(url)

  links = []

  for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
      #print 'inside if of href'
      url = link['href']
      #match = re.search(r'http://www.homeshop18.com/[\w\s\d-]+/author:[\w\d-]+/isbn:\d+/books/'+category4url+'/product:\d+/cid:\d+/',str(link))
      match = re.search(r'http://www.homeshop18.com/[\w\s\d-]+/author:[\w\d-]+/isbn:\d+/books/[\w\d-]+/product:\d+/cid:\d+/',str(link))
      if match:
        url = url.replace("</a>","")
        print match.group()
        links.append(url)
          
        scraperwiki.sqlite.save(["url","category"],{'url':url,'category':category},"swdata")
          
print len(links)
print type(links)


  
