import scraperwiki
import time
import re
from bs4 import BeautifulSoup
from collections import namedtuple

def parse_date(strDate):
    try:
        return time.strptime(strDate, "%d %B %Y")
    except:
        pass
    
    try:
        return time.strptime(strDate, "%d %B%Y")
    except:
        pass
    
    try:
        return time.strptime(strDate, "%d%B%Y")
    except:
        return time.strftime("1 January 2000", "%d %B %Y")

def parse_text(col):
    col = [" ".join(x.split()) for x in col]
    return " ".join(col)

def get_conviction_details(url):
    prefix = 'http://docs.health.vic.gov.au/docs/doc/'
    response = scraperwiki.scrape(url)
    soup = BeautifulSoup(response)
    div_entry = soup.find(class_='entry')
    doc_url = div_entry.find('a').get('href')
    return prefix + doc_url  

response = scraperwiki.scrape('http://www.health.vic.gov.au/foodsafety/regulatory_info/register.htm')
soup = BeautifulSoup(response)
conviction_table = soup.find_all('table', class_="stdTable")[0]

for tr in conviction_table.findAll('tr'):
    col = tr.findAll('td')
    if col:
        data = {
            'name':  parse_text(col[1].findAll(text=True)),
            'address': parse_text(col[3].findAll(text=True)),
            'date': parse_date(col[5].string.strip()),
            'details': get_conviction_details(col[6].find('a').get('href'))
        }
        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=data)

import scraperwiki
import time
import re
from bs4 import BeautifulSoup
from collections import namedtuple

def parse_date(strDate):
    try:
        return time.strptime(strDate, "%d %B %Y")
    except:
        pass
    
    try:
        return time.strptime(strDate, "%d %B%Y")
    except:
        pass
    
    try:
        return time.strptime(strDate, "%d%B%Y")
    except:
        return time.strftime("1 January 2000", "%d %B %Y")

def parse_text(col):
    col = [" ".join(x.split()) for x in col]
    return " ".join(col)

def get_conviction_details(url):
    prefix = 'http://docs.health.vic.gov.au/docs/doc/'
    response = scraperwiki.scrape(url)
    soup = BeautifulSoup(response)
    div_entry = soup.find(class_='entry')
    doc_url = div_entry.find('a').get('href')
    return prefix + doc_url  

response = scraperwiki.scrape('http://www.health.vic.gov.au/foodsafety/regulatory_info/register.htm')
soup = BeautifulSoup(response)
conviction_table = soup.find_all('table', class_="stdTable")[0]

for tr in conviction_table.findAll('tr'):
    col = tr.findAll('td')
    if col:
        data = {
            'name':  parse_text(col[1].findAll(text=True)),
            'address': parse_text(col[3].findAll(text=True)),
            'date': parse_date(col[5].string.strip()),
            'details': get_conviction_details(col[6].find('a').get('href'))
        }
        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=data)

