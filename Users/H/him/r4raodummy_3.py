import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)
    title = tree.find('.//h1')
    price = tree.find('.//span[@class="fk-font-finalprice"]')
    data = {
        'title': title.text if title is not None else '',
        'url': url,
        'price': price.text_content() if price is not None else ''
    }
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

start = 0
while start<420:
    listPage = scraperwiki.scrape('http://www.flipkart.com/books/educational-and-professional/academic-and-professional/school/pr?p%5B%5D=sort%3Dpopularity&sid=bks%2Cenp%2Cq2s%2Czze&start=%d' % start)
    tree = lxml.html.fromstring(listPage)
    for link in tree.findall('.//a[@class="pu-image fk-product-thumb "]'):
        url = link.get('href', '')
        if not url:
            continue
        parsed_url = urlparse.urlparse(url)
        print parsed_url.path
        scrape_laptop('http://www.flipkart.com' + parsed_url.path)
    start += 20
