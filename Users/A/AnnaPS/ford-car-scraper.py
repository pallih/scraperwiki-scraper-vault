###############################################################################
# Scrape Ford car information
###############################################################################

import scraperwiki
import mechanize
import re
import sys
from BeautifulSoup import BeautifulSoup

def get_model_details(car_name, model_url):
    br = mechanize.Browser()
    html = br.open(model_url).read()
    soup = BeautifulSoup(html)
    record = {}
    headers = soup.find('thead').find('tr').findAll('th')
    header_text = headers[1].findAll(text=True)
    model = header_text[0]
    price = header_text[1]
    print model, price
    record['car_name'] = car_name
    record['model'] = model
    record['price'] = price
    print model, price
    trs = soup.find('tbody').findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        if tds[1].text=='Standard' or tds[1].text=='Not available':
            pass
        else:
            print tds[0].text, tds[1].text
            record[tds[0].text] = tds[1].text
    return record
    
starting_url = 'http://www.ford.co.uk/Cars'
br = mechanize.Browser()
html = br.open(starting_url).read()
links = re.findall("link: '/Hidden([^']+)'", html)
base_url = 'http://www.ford.co.uk/Hidden'
for link in links:
    model_url = base_url + link
    car_name = re.match("/SidebySide([^']+)/", link)
    car_name = car_name.group().replace('/SidebySide', '')
    car_name = car_name.replace('/', '')
    print car_name
    record = get_model_details(car_name, model_url)
    scraperwiki.datastore.save(["price"], record) 
    
