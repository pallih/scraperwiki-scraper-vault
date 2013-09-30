import scraperwiki
import re
from lxml import html
from lxml import etree

def get_image(uri, url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    images = article.pop().cssselect("img")

    if len(images) > 0:
        
        for image in images:

            print image

            src_full = image.get("src")
            print src_full
    
            data = {
                'image': src_full.strip(),
            }

            scraperwiki.sqlite.save(unique_keys=["image"], data=data)


def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.xpath('//*[@id="menu"]/div/ul[1]/li[4]/div/div[2]/div/div/ul/li'):
    uri = link.cssselect('a').pop().get('href')
    product = link.cssselect('span').pop().text_content()
    href = url+uri
    get_image(uri, href, product)

    import scraperwiki
import re
from lxml import html
from lxml import etree

def get_image(uri, url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    images = article.pop().cssselect("img")

    if len(images) > 0:
        
        for image in images:

            print image

            src_full = image.get("src")
            print src_full
    
            data = {
                'image': src_full.strip(),
            }

            scraperwiki.sqlite.save(unique_keys=["image"], data=data)


def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.xpath('//*[@id="menu"]/div/ul[1]/li[4]/div/div[2]/div/div/ul/li'):
    uri = link.cssselect('a').pop().get('href')
    product = link.cssselect('span').pop().text_content()
    href = url+uri
    get_image(uri, href, product)

    