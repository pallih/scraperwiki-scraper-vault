import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import urllib

## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, title, link, pubDate from `swdata` order by pubDate desc limit 10

TERMS = ["eggleston", "lee+friedlander", "winogrand", "new+topographics", "koudelka", "alex+webb", "joel+meyerowitz", "fred+herzog", "henry+wessel", "ghirri", "walker+evans", "mitch+epstein", "mermelstein", "steidl", "phaidon", "martin+parr", "david+alan+harvey", "Economopoulos", "mark+steinmetz", "vanessa+winship", "eugene+richards"]

exASINs = scraperwiki.sqlite.select("ASIN from swdata limit 100")
exASINs = tuple((i['ASIN']) for i in exASINs)
#exASINs = [] ## needed after datastore is cleared

now = datetime.datetime.now()


for term in TERMS:
  url = "http://www.amazon.de/s/rss/ref=nb_sb_noss?__mk_de_DE=%C5M%C5Z%D5%D1&url=me%3DA8KICS1PHF7ZO&field-keywords=" + term
  f = urllib.urlopen(url)
  html = f.read()
  f.close
  root = lxml.html.fromstring(html)
  for result in root.xpath("descendant-or-self::div[starts-with(@id, 'result_')]"):
    for title in result.cssselect('div[class=\"productTitle\"]'):
      Title = title.text_content()
    for link in result.cssselect('div[class=\"productTitle\"] a'):
      Link = link.get('href')
    for img in result.cssselect('div[class=\"productTitle\"] img'):
      Img = img.get('src')
    for price in result.cssselect('div[class=\"usedPrice\"] span'):
      Price = price.text.replace("EUR ", "")
    ASIN = Link[-10:]
    Description = Title + ' for EUR ' + Price
    if not(ASIN in exASINs):
      item = {
        'ASIN': ASIN,
        'title': Title,
        'link': Link,
        'img': Img,
        'price': Price,
        'pubDate': str(now) ,
        'description': Description,
      }
      scraperwiki.sqlite.save(unique_keys=['ASIN', 'price'],data=item)

## delete old entries
scraperwiki.sqlite.execute("delete from swdata where date(pubDate) < date('now', '-14 day')")
