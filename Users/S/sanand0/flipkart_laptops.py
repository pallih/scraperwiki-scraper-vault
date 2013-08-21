import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)
    title = tree.find('.//h1')
    price = tree.find('.//span[@id="fk-mprod-our-id"]')
    data = {
        'title': title.text if title is not None else '',
        'url': url,
        'price': price.text_content() if price is not None else ''
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
    data = scraperwiki.scrape('http://www.flipkart.com/computers/laptops/all?response-type=json&inf-start=%d' % start)
    data = json.loads(data)
    if data['count'] <= 0:
        break
    tree = lxml.html.fromstring(data['html'])
    for link in tree.findall('.//a[@class="prd-img"]'):
        url = link.get('href', '')
        if not url:
            continue
        parsed_url = urlparse.urlparse(url)
        print parsed_url.path
        scrape_laptop('http://www.flipkart.com' + parsed_url.path)
    start += 20
