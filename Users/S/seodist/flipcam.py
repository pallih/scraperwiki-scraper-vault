# FlipKart Python
import scraperwiki
import json
import re
import urlparse
from lxml import etree

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = etree.HTML(html)
    title = tree.find('.//h1')
    data = {
        'title': title.text if title is not None else '',
        'url': url,
    }
    for row in tree.findall('.//table[@class="fk-specs-type2"]//tr'):
        label = row.find('th')
        value = row.find('td')
        if label is not None and value is not None and label.text is not None:
            # Ensure key is simple text. 
            key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)
            data[key] = value.text
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

start = 0
while True:
    data = scraperwiki.scrape('http://www.flipkart.com/cameras/all-digital-cameras?response-type=json&inf-start=%d' % start)
    data = json.loads(data)
    if data['count'] <= 0:
        break
    tree = etree.HTML(data['html'])
    for link in tree.findall('.//a[@class="prd-img"]'):
#for link in tree.findall('.//a[@class="fk-product-thumb fkp-medium"]'):
        url = link.get('href', '')
        #price = link.get('.//span[@class="price final-price"]')
        print  price
        if not url:
            continue
        parsed_url = urlparse.urlparse(url)
        print parsed_url.path
        scrape_laptop('http://www.flipkart.com' + parsed_url.path)
        start += 20

# FlipKart Python
import scraperwiki
import json
import re
import urlparse
from lxml import etree

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = etree.HTML(html)
    title = tree.find('.//h1')
    data = {
        'title': title.text if title is not None else '',
        'url': url,
    }
    for row in tree.findall('.//table[@class="fk-specs-type2"]//tr'):
        label = row.find('th')
        value = row.find('td')
        if label is not None and value is not None and label.text is not None:
            # Ensure key is simple text. 
            key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)
            data[key] = value.text
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

start = 0
while True:
    data = scraperwiki.scrape('http://www.flipkart.com/cameras/all-digital-cameras?response-type=json&inf-start=%d' % start)
    data = json.loads(data)
    if data['count'] <= 0:
        break
    tree = etree.HTML(data['html'])
    for link in tree.findall('.//a[@class="prd-img"]'):
#for link in tree.findall('.//a[@class="fk-product-thumb fkp-medium"]'):
        url = link.get('href', '')
        #price = link.get('.//span[@class="price final-price"]')
        print  price
        if not url:
            continue
        parsed_url = urlparse.urlparse(url)
        print parsed_url.path
        scrape_laptop('http://www.flipkart.com' + parsed_url.path)
        start += 20

