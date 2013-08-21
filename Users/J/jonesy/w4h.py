import scraperwiki
import re
from lxml import html
from lxml import etree

def get_product_details(uri):
    
    doc_text = scraperwiki.scrape("http://www.water-for-health.co.uk"+uri)
    doc = html.fromstring(doc_text)

    name = doc.cssselect("h1")[0]

    # get category id(s)

    url_parts = uri.split('/')
    total = len(url_parts)  
    sub = url_parts[total-2] 

    subccategory = sub.split('-')[0]
    
    price_lst = doc.cssselect("span.productPrice")
    
    if(len(price_lst) > 0):
        price = price_lst[0].text
        price = price.replace("&pound;", "")
    else:
        price = ''

    old_price_lst = doc.cssselect("span.product-Old-Price")

    if(len(old_price_lst ) > 0):
        old_price = old_price_lst [0].text
    else:
        old_price = ''

    product_id_lst = doc.cssselect('input[name="product_id"]')
    
    if(len(product_id_lst) > 0):
        product_id = product_id_lst[0].get("value")
    else:
        product_id = None

    image_lst = doc.cssselect("table > tbody > tr > td a")


    if(len(image_lst) > 0):
        image = image_lst[0]
        src_full = image.get("href")
        src = src_full.split('/')[-1]
    else:
        src = ''

    # now get description

    h1 = doc.cssselect("td > h1")
    if(len(h1) > 0):
        if(len(h1) == 1):
            index = 0
        else:
            index = 1

        td = h1[index].getparent()
        description = html.tostring(td)
        description = re.sub(r'(<td colspan="2">|<td bordercolor="#B2E3FA" bgcolor="#B2E3FA">)', '', description)
        description = re.sub(r'</td>', '', description)
    else:
        description = ''
   
    data = {
        'product_id': product_id.strip(' \t\n\r'),
        'name': name.text.strip(' \t\n\r'),
        'price': price.strip(),
        'old_price': old_price.strip(' \t\n\r'),
        'image': src.strip(),
        'subcategory': subccategory,
        'description': description.strip(' \t\n\r'),
    }

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

url = "http://www.water-for-health.co.uk/site-map.html"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for product in doc.cssselect("ul.level_3 > li"):
    
    for link in product.cssselect("a"):
        get_product_details(link.get('href'))

    