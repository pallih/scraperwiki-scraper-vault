import scraperwiki
import re
from lxml import html
from lxml import etree

def get_product_details(uri):
    
    doc_text = scraperwiki.scrape("http://www.water-for-health.co.uk"+uri)
    doc = html.fromstring(doc_text)

    image_lst = doc.cssselect("table > tbody > tr > td a")


    if(len(image_lst) > 0):
        image = image_lst[0]
        src_full = image.get("href")
        print src_full

    data = {
        'image': src_full.strip(),
    }

    scraperwiki.sqlite.save(unique_keys=["image"], data=data)

url = "http://www.water-for-health.co.uk/site-map.html"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for product in doc.cssselect("ul.level_3 > li"):
    
    for link in product.cssselect("a"):
        get_product_details(link.get('href'))

    import scraperwiki
import re
from lxml import html
from lxml import etree

def get_product_details(uri):
    
    doc_text = scraperwiki.scrape("http://www.water-for-health.co.uk"+uri)
    doc = html.fromstring(doc_text)

    image_lst = doc.cssselect("table > tbody > tr > td a")


    if(len(image_lst) > 0):
        image = image_lst[0]
        src_full = image.get("href")
        print src_full

    data = {
        'image': src_full.strip(),
    }

    scraperwiki.sqlite.save(unique_keys=["image"], data=data)

url = "http://www.water-for-health.co.uk/site-map.html"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for product in doc.cssselect("ul.level_3 > li"):
    
    for link in product.cssselect("a"):
        get_product_details(link.get('href'))

    