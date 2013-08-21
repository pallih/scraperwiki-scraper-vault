'''Pulls data in from www.amfikenya.com for Microfinance Information eXchange'''

import BeautifulSoup
import requests
import re
#import json
from scraperwiki.sqlite import save
from time import time
DATE = time()

def scrape_raw(url):
  __d = requests.get(url)
  _d = re.sub('<br[^>]*>','|',__d.content)
  _d = re.sub('[\r\n]','',_d)
  d = BeautifulSoup.BeautifulSoup(_d)
  return d.findAll(['td','font'], attrs={'face': 'verdana'})

def kindofint(t):
    try:
        i =  int(t)
        return True
    except:
        return False

def parse_rows(l):
  out = []
  record = None
  for row in l:
     t = row.text
     if kindofint(t):
        if record != None: out.append(record)
        record = []
     if record != None:
        record.append(t)
    
  out.append(record)  
  return out

def parse_record(l):
    out = {}
    out['id'] = l[0]
    out['name'] = l[1]
    out['country'] = 'Kenya'
    out['type'] = 'MFI'
    out['source'] = 'Direct Website'
    try:out['url'] = l[3]
    except IndexError:out['url'] = ''
    _address_area = l[2].split('|')
    address = []
    contact = []
    hitContact = False
    for row in _address_area:
        if re.findall('^tel|^mobile|^fax|^.*@', row, re.IGNORECASE) != []:
            hitContact = True 
        if not hitContact:
            address.append(row)
        else:
            contact.append(row)
    out['address'] = ','.join(address)
    out['contact'] = ','.join(contact)
    return out
       

def main():
    url = 'http://www.amfikenya.com/pages.php?p=3'
    #outfile = open('amfikenya.json','w')
    d = scrape_raw(url)
    out = map(parse_record, parse_rows(d))
    #json.dump(out,outfile)
    for row in out:
        row['date_scraped'] = DATE
    save([], out)


main()