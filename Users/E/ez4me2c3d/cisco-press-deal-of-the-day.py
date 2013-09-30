from BeautifulSoup import BeautifulSoup
import scraperwiki
import time

# Base URL
url = 'http://www.ciscopress.com/deals/index.asp'

# Get the current timestamp
scrape_datetime  = int(time.mktime(time.localtime()))
    
# Grab the web page
html_resp = scraperwiki.scrape(url)
    
# Use BeautifulSoup to parse the HTML and create a tree
html_tree = BeautifulSoup(html_resp)
    
# Extract only the product item record and it's attributes: info and price
item  = html_tree.find('div', {'id': 'contentProduct'}) 
title = item.find('h1', {'id': 'productTitle'}).string.strip()
info  = item.find('div', {'id': 'moreInfo'}).find('p').string.strip()
price = item.find('p', {'class': 'productMessageFull'}).find('strong').string.strip().replace('$', '')

#print scrape_datetime, title, info, price
scraperwiki.sqlite.save(['timestamp', 'title'], {'timestamp' : scrape_datetime, 'title' : title, 'info' : info, 'price' : price})from BeautifulSoup import BeautifulSoup
import scraperwiki
import time

# Base URL
url = 'http://www.ciscopress.com/deals/index.asp'

# Get the current timestamp
scrape_datetime  = int(time.mktime(time.localtime()))
    
# Grab the web page
html_resp = scraperwiki.scrape(url)
    
# Use BeautifulSoup to parse the HTML and create a tree
html_tree = BeautifulSoup(html_resp)
    
# Extract only the product item record and it's attributes: info and price
item  = html_tree.find('div', {'id': 'contentProduct'}) 
title = item.find('h1', {'id': 'productTitle'}).string.strip()
info  = item.find('div', {'id': 'moreInfo'}).find('p').string.strip()
price = item.find('p', {'class': 'productMessageFull'}).find('strong').string.strip().replace('$', '')

#print scrape_datetime, title, info, price
scraperwiki.sqlite.save(['timestamp', 'title'], {'timestamp' : scrape_datetime, 'title' : title, 'info' : info, 'price' : price})