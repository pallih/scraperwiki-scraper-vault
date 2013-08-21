import scraperwiki
import lxml.html

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

products = ['http://www.mysupermarket.co.uk/#/tesco-price-comparison/soft_drinks/coca_cola_2l.html',
            'http://www.mysupermarket.co.uk/#/tesco-price-comparison/tinned_tomatoes_puree_and_passata/napolina_chopped_tomatoes_in_tomato_juice_4x400g.html']

def scrape(url):
    root = fetch_html(url)
    print root
    for supermarket in root.find_class('StoreDiv'):
        print supermarket

for prod in products:
    scrape(prod)    