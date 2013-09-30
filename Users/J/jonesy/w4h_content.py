import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    if len(article) > 0:
        text = innerHTML(article[0])
        print text

        data = {
            'product':product,
            'content': text,
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.cssselect("#contentleft ul.menu li.level1 a"):
    product = link.text_content()
    href = url+link.get('href')
    get_content(href, product)

    import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    if len(article) > 0:
        text = innerHTML(article[0])
        print text

        data = {
            'product':product,
            'content': text,
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.cssselect("#contentleft ul.menu li.level1 a"):
    product = link.text_content()
    href = url+link.get('href')
    get_content(href, product)

    