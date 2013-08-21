import scraperwiki
import lxml.html
import lxml.etree
import pprint       
import re

categories = []
import requests
import base64
# Blank Python

def get_categories(start_url = None):
    html = scraperwiki.scrape(start_url or "http://www.yourfashionjewellery.com/Costume-Jewellery/")
    root = lxml.html.fromstring(html)
    for category_container in root.find_class("subcategories"):
        
        for category_link in category_container.iter("a"):
            if len(category_link): continue
            
            data = { 
                "href": category_link.get('href'), 
                "name": category_link.text_content()
            }
            categories.append(data)
            scraperwiki.sqlite.save(unique_keys=["href"], data=data, table_name="categories", verbose=2)
    
def scrape_category_pages():
    for category_page in categories:
        print pprint.pformat(category_page['name'])

        html = scraperwiki.scrape(category_page['href'] + "?objects_per_page=50")
        document = lxml.html.fromstring(html)
        for item_holder in document.cssselect(".cf > div[align='center']"):
            data = { 'category': category_page['name'] }
            
            
            data['image_url'] = list(item_holder.iterdescendants('img'))[0].get('src')
            data['image'] = base64.b64encode( requests.get(data['image_url']).content )

            data['url'] = item_holder[1][1].get('href')
            
            data['name'] = "".join(item_holder[1][1][0].itertext())
            data['price'] = "".join(item_holder[1][1][3].itertext())

            scraperwiki.sqlite.save(unique_keys=["url"], data=data, table_name="products", verbose=2)

root = lxml.html.fromstring(scraperwiki.scrape("http://www.yourfashionjewellery.com"))
for area in root.cssselect('ul.eviesul li a, ul.fancycat-icons-level-0 li a'):
    print area.text
    url = area.get('href')
    if not url.startswith("http://"):
        url = "http://www.yourfashionjewellery.com/" + url
    get_categories(url)

scrape_category_pages()


