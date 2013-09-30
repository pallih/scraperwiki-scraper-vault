import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import time
import urllib2


## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, description as title, link, scraped as pubDate from `swdata` order by pubDate desc limit 60

URLS = ["koeln-bonn-cgn/pisa-psa/juli-2013.htm", "pisa-psa/koeln-bonn-cgn/august-2013.htm"]

user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101\Firefox/7.0.1"
headers = {'User-Agent':user_agent}

for urlpart in URLS:
  url = "http://www.germanwings.com/de/Angebote/Flugangebote/guenstige-fluege/" + urlpart
  print "trying " + url
  req = urllib2.Request(url=url,headers=headers)
  html = urllib2.urlopen(req).read()
  print "read html..."
  root = lxml.html.fromstring(html)
  
  dirsplit = [i.split('-') for i in urlpart.split('/')]
  from_dir = dirsplit[0][-1]
  to_dir = dirsplit[1][-1]
  direction = from_dir + to_dir
  
  for result in root.xpath("descendant-or-self::li[starts-with(@class, 'qtr ')]"):
    print "try a result..."
    try:
      date = result.cssselect("span[class='dtstart']")[0].text
      price = result.cssselect("span[class='price']")[0].text
      price = price.replace(u" \u20ac", "")
      price = price.replace(",", ".")
      price = round(float(price), 2)
      now = datetime.datetime.now()
      item = {
        'date': date,
        'price': price,
        'direction': direction,
        'scraped': str(now),
      }
      scraperwiki.sqlite.save(unique_keys=['date', 'scraped'], data=item)
    except:
      pass
import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import time
import urllib2


## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, description as title, link, scraped as pubDate from `swdata` order by pubDate desc limit 60

URLS = ["koeln-bonn-cgn/pisa-psa/juli-2013.htm", "pisa-psa/koeln-bonn-cgn/august-2013.htm"]

user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101\Firefox/7.0.1"
headers = {'User-Agent':user_agent}

for urlpart in URLS:
  url = "http://www.germanwings.com/de/Angebote/Flugangebote/guenstige-fluege/" + urlpart
  print "trying " + url
  req = urllib2.Request(url=url,headers=headers)
  html = urllib2.urlopen(req).read()
  print "read html..."
  root = lxml.html.fromstring(html)
  
  dirsplit = [i.split('-') for i in urlpart.split('/')]
  from_dir = dirsplit[0][-1]
  to_dir = dirsplit[1][-1]
  direction = from_dir + to_dir
  
  for result in root.xpath("descendant-or-self::li[starts-with(@class, 'qtr ')]"):
    print "try a result..."
    try:
      date = result.cssselect("span[class='dtstart']")[0].text
      price = result.cssselect("span[class='price']")[0].text
      price = price.replace(u" \u20ac", "")
      price = price.replace(",", ".")
      price = round(float(price), 2)
      now = datetime.datetime.now()
      item = {
        'date': date,
        'price': price,
        'direction': direction,
        'scraped': str(now),
      }
      scraperwiki.sqlite.save(unique_keys=['date', 'scraped'], data=item)
    except:
      pass
