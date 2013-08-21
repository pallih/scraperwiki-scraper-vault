from BeautifulSoup import BeautifulSoup
import scraperwiki
import time
import re

# Base URL for the Apple Refurb Store
url_refurb_store = 'http://store.apple.com/us/browse/home/specialdeals/mac/'

# A list of products to scrape
products = [
    {
        'enabled': True,
        'name': 'macbook',
        'url': url_refurb_store + 'macbook/'
    },
    {
        'enabled': True,
        'name': 'macbook_pro',
        'url': url_refurb_store + 'macbook_pro/'
    },
    {
        'enabled': True,
        'name': 'macbook_air',
        'url': url_refurb_store + 'macbook_air/'
    },
    {
        'enabled': True,
        'name': 'imac',
        'url': url_refurb_store + 'imac/'
    },
    {
        'enabled': True,
        'name': 'mac_pro',
        'url': url_refurb_store + 'mac_pro/'
    },
    {
        'enabled': True,
        'name': 'mac_mini',
        'url': url_refurb_store + 'mac_mini/'
    },
    {
        'enabled': True,
        'name': 'xserve',
        'url': url_refurb_store + 'xserve/'
    },
    {
        'enabled': True,
        'name': 'displays',
        'url': url_refurb_store + 'displays/'
    }
]

for product in products:
    # Only scrape pages for enabled products
    if not product['enabled']:
           continue
    
    # Get the current timestamp
    scrape_datetime  = int(time.mktime(time.localtime()))
    
    # Grab the web page
    html_resp        = scraperwiki.scrape(product['url'])
    
    # Use BeautifulSoup to parse the HTML and create a tree
    html_tree        = BeautifulSoup(html_resp)
    
    # Extract only the product item records (tr elements with 'product' in the class list)
    items            = html_tree.findAll('tr', {'class' : re.compile("product", re.IGNORECASE)})
    
    # Iterate over each product item found, extracting the model, description, and price, then store the data with a timestamp
    for item in items:
        model       = re.compile("product/(.*?)/").search(item.find('h3').find('a')['href']).group(1)
        description = item.find('h3').find('a').string.strip()
        price       = item.find('p', {'class' : 'price'}).find('span', {'class' : 'current_price'}).string.strip().replace('$', '').replace(',', '')
        
        #print scrape_datetime, product['name'], model, description, price
        scraperwiki.sqlite.save(['timestamp', 'product', 'model'], {'timestamp' : scrape_datetime, 'product' : product['name'], 'model' : model, 'description' : description, 'price' : price})
    