import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import time
import urllib


## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, description as title, link, scraped as pubDate from `swdata` order by pubDate desc limit 60

URLS = ["koeln-bonn-cgn/pisa-psa/juli-2013.htm", "pisa-psa/koeln-bonn-cgn/august-2013.htm"]

for urlpart in URLS:
  url = "http://www.germanwings.com/de/Angebote/Flugangebote/guenstige-fluege/" + urlpart
  print "trying " + url
  f = urllib.urlopen(url)
  html = f.read()
  f.close
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
      title = result.cssselect("span[class='summary description']")[0].text
      description = direction + " am " + date + " fuer " + str(price) + " EUR"
      now = datetime.datetime.now()
      item = {
        'date': date,
        'price': price,
        'direction': direction,
        'scraped': str(now),
        'title': title,
        'description': description,
        'link': url,
      }
      scraperwiki.sqlite.save(unique_keys=['direction', 'date', 'price'], data=item)
    except:
      pass
