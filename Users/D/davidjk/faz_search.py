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
## select description, title, link, pubDate from `swdata` order by pubDate desc limit 10

TOPICS = ["leica", "grundschule", "fusion", "kartell"]

AUTHORS = ["dietmar+dath", "frank+rieger"]

AUTHORS = ["&author=" + x for x in AUTHORS]

TERMS = TOPICS + AUTHORS

for term in TERMS:
  url = "http://www.faz.net/suche/?query=" + term
  f = urllib.urlopen(url)
  html = f.read()
  f.close
  root = lxml.html.fromstring(html)
  for result in root.xpath("descendant-or-self::div[@class='SuchergebnisListe']/descendant-or-self::*/div[starts-with(@class, 'Teaser620')]"):
    ## check whether we found archived results
    klasse = result.attrib['class']
    if not("Archiv" in klasse):
      info = result.cssselect("a[class = 'LinkMehr']")
      title = info[0].get("title")
      url = info[0].get("href")
      link = "http://www.faz.net" + url
    
      date = result.cssselect("span[class = 'Date']")[0].text
      pubDate = datetime.datetime.strptime(date, "%d.%m.%y %H:%M")
    
      description = title + " um " + date
    
      item = {
        'title': title,
        'link': link,
        'pubDate': str(pubDate),
        'description': description,
        }
      scraperwiki.sqlite.save(unique_keys=['pubDate'], data=item)

    else:
      break