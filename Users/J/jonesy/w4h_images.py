import scraperwiki
import re
from lxml import html
from lxml import etree

def get_images(url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    images = doc.cssselect("div.article img")

    ignore = ['menu_logo.gif', 'onlineshop.jpg', 'ebookletbanner.jpg', 'jlg.jpg', 'cataloguelink.png', 'onlineshop.PNG', 'JLG.jpg']

    for image in images:
        src = image.get("src")

        src = src.split("/")

        if any(src[-1] in s for s in ignore):
            continue

        data = {
            'product':product,
            'image': src[-1]
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.cssselect("#contentleft ul.menu li.level1 a"):
    product = link.text_content()
    href = url+link.get('href')
    get_images(href, product)

    import scraperwiki
import re
from lxml import html
from lxml import etree

def get_images(url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    images = doc.cssselect("div.article img")

    ignore = ['menu_logo.gif', 'onlineshop.jpg', 'ebookletbanner.jpg', 'jlg.jpg', 'cataloguelink.png', 'onlineshop.PNG', 'JLG.jpg']

    for image in images:
        src = image.get("src")

        src = src.split("/")

        if any(src[-1] in s for s in ignore):
            continue

        data = {
            'product':product,
            'image': src[-1]
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.cssselect("#contentleft ul.menu li.level1 a"):
    product = link.text_content()
    href = url+link.get('href')
    get_images(href, product)

    