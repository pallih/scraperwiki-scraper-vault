import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import time
import urllib2
import re

## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, title, link, pubDate from `swdata` order by pubDate desc limit 10

ASINS = ["1935004085", "8869651398", "3791339605", "1935202073", "0953890120", "0953890104", "3931141365", "193443518X", "1597110345", "1580930964", "0385266510", "1597111732", "1888899093", "1576872521", "386930135X"]

user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101\Firefox/7.0.1"
headers = {'User-Agent':user_agent}

now = datetime.datetime.now()

for asin in ASINS:
  url = "http://www.amazon.de/gp/offer-listing/" + asin + "/"
  req = urllib2.Request(url=url,headers=headers)
  html = urllib2.urlopen(req).read()
  root = lxml.html.fromstring(html)
  title = root.cssselect("h1[class='producttitle']")[0].text
  for result in root.cssselect("tbody[class='result']"):
    price_raw = result.cssselect("span[class='price']")[0].text
    price = price_raw.replace(".","").replace(",",".").split(" ")[1]
    condition_raw = result.cssselect("div[class='condition']")[0].text.replace("\n", "")
    condition = re.sub(r'\s+', r' ', condition_raw).strip()
    try:
      seller = result.cssselect("div[class='seller'] a b")[0].text
      shipping_raw = result.cssselect("span[class='price_shipping']")[0].text
      shipping = re.findall(r'\d+,\d+', shipping_raw)[0].replace(",", ".")
      avail_raw = result.cssselect("div[class='availability']")[0].text.replace("\n", "")
      availability = re.sub(r'\s+', r' ', avail_raw).strip()
      try: ## maybe new seller
        stars_img = result.cssselect("div[class='rating'] img")[0].get("src")
        stars = re.findall(r'stars-(\d-\d)', stars_img)[0].replace("-",".")
        rating_perc = result.cssselect("div[class='rating'] b")[0].text
        rating_perc = rating_perc.split("%")[0]
      except:
        stars = "NA"
        rating_perc = "NA"
      offerID = result.cssselect("input[name='offeringID.1']")[0].get("value")
    except:
      seller = "Amazon"
      stars = "NA"
      rating_perc = "NA"
      shipping = "0"
      offerID = "AZN" + asin
      availability = "Amazon"
    item = {
      'ASIN': asin,
      'title': title,
      'price': price,
      'shipping': shipping,
      'condition': condition,
      'seller': seller,
      'stars': stars,
      'rating': rating_perc,
      'offerID': offerID,
      'scraped': str(now),
      'availability': availability,
    }
    scraperwiki.sqlite.save(unique_keys=['offerID', 'scraped'], data=item)
import scraperwiki
import lxml.html 
import lxml.cssselect
import uuid
import datetime
import time
import urllib2
import re

## anleitung:
## http://wisepricer.com/blog/hack-price-monitoring-with-ifttt-and-scraperwiki/

## feed select statement:
## select description, title, link, pubDate from `swdata` order by pubDate desc limit 10

ASINS = ["1935004085", "8869651398", "3791339605", "1935202073", "0953890120", "0953890104", "3931141365", "193443518X", "1597110345", "1580930964", "0385266510", "1597111732", "1888899093", "1576872521", "386930135X"]

user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101\Firefox/7.0.1"
headers = {'User-Agent':user_agent}

now = datetime.datetime.now()

for asin in ASINS:
  url = "http://www.amazon.de/gp/offer-listing/" + asin + "/"
  req = urllib2.Request(url=url,headers=headers)
  html = urllib2.urlopen(req).read()
  root = lxml.html.fromstring(html)
  title = root.cssselect("h1[class='producttitle']")[0].text
  for result in root.cssselect("tbody[class='result']"):
    price_raw = result.cssselect("span[class='price']")[0].text
    price = price_raw.replace(".","").replace(",",".").split(" ")[1]
    condition_raw = result.cssselect("div[class='condition']")[0].text.replace("\n", "")
    condition = re.sub(r'\s+', r' ', condition_raw).strip()
    try:
      seller = result.cssselect("div[class='seller'] a b")[0].text
      shipping_raw = result.cssselect("span[class='price_shipping']")[0].text
      shipping = re.findall(r'\d+,\d+', shipping_raw)[0].replace(",", ".")
      avail_raw = result.cssselect("div[class='availability']")[0].text.replace("\n", "")
      availability = re.sub(r'\s+', r' ', avail_raw).strip()
      try: ## maybe new seller
        stars_img = result.cssselect("div[class='rating'] img")[0].get("src")
        stars = re.findall(r'stars-(\d-\d)', stars_img)[0].replace("-",".")
        rating_perc = result.cssselect("div[class='rating'] b")[0].text
        rating_perc = rating_perc.split("%")[0]
      except:
        stars = "NA"
        rating_perc = "NA"
      offerID = result.cssselect("input[name='offeringID.1']")[0].get("value")
    except:
      seller = "Amazon"
      stars = "NA"
      rating_perc = "NA"
      shipping = "0"
      offerID = "AZN" + asin
      availability = "Amazon"
    item = {
      'ASIN': asin,
      'title': title,
      'price': price,
      'shipping': shipping,
      'condition': condition,
      'seller': seller,
      'stars': stars,
      'rating': rating_perc,
      'offerID': offerID,
      'scraped': str(now),
      'availability': availability,
    }
    scraperwiki.sqlite.save(unique_keys=['offerID', 'scraped'], data=item)
