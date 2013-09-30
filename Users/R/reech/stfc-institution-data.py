import sys
import traceback
import re
from datetime import datetime
import time
from scraperwiki import datastore
import scraperwiki
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.scitech.ac.uk'
full_list_url = 'http://www.stfc.ac.uk/GOW/Sm/Inst.asp?cx=01&sc=0&so=oa'

# Fetch and Store STFC grant institution data - used in STFC_GRANTS scraper
def main():
    # print scraperwiki.geo.os_easting_northing_to_latlng(702997,5716856)
    list_page = BeautifulSoup(scraperwiki.scrape(full_list_url))
    parse_orgs(list_page)
    
    

def parse_orgs(institution_list):
    
    ins = institution_list.findAll('tr', {'class':'tHigh', 'class':'tLow', })
    
    cls_map = {'dc2':'institution', 'dc4':'current_grants', 'dc5':'announced_grants_total', }
    # loop through all rows
    for i in ins: 
        institution = {}
        link = i.find('a', {'class':'noUndStd'})
        institution['stfc_url'] = base_url + link['href']
        institution['id'] = re.match('.*in=(-?\d+)$',institution['stfc_url']).group(1)
        print institution['id'] 
        
        for cell_cls, name in cls_map.iteritems():
            institution[name] = i.find('td', {'class':cell_cls}).text.strip()
            
        institution['announced_grants_total']  = int(institution['announced_grants_total'].replace(',',''))
        datastore.save(unique_keys=['id'], data=institution)
        print institution

main()
import sys
import traceback
import re
from datetime import datetime
import time
from scraperwiki import datastore
import scraperwiki
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.scitech.ac.uk'
full_list_url = 'http://www.stfc.ac.uk/GOW/Sm/Inst.asp?cx=01&sc=0&so=oa'

# Fetch and Store STFC grant institution data - used in STFC_GRANTS scraper
def main():
    # print scraperwiki.geo.os_easting_northing_to_latlng(702997,5716856)
    list_page = BeautifulSoup(scraperwiki.scrape(full_list_url))
    parse_orgs(list_page)
    
    

def parse_orgs(institution_list):
    
    ins = institution_list.findAll('tr', {'class':'tHigh', 'class':'tLow', })
    
    cls_map = {'dc2':'institution', 'dc4':'current_grants', 'dc5':'announced_grants_total', }
    # loop through all rows
    for i in ins: 
        institution = {}
        link = i.find('a', {'class':'noUndStd'})
        institution['stfc_url'] = base_url + link['href']
        institution['id'] = re.match('.*in=(-?\d+)$',institution['stfc_url']).group(1)
        print institution['id'] 
        
        for cell_cls, name in cls_map.iteritems():
            institution[name] = i.find('td', {'class':cell_cls}).text.strip()
            
        institution['announced_grants_total']  = int(institution['announced_grants_total'].replace(',',''))
        datastore.save(unique_keys=['id'], data=institution)
        print institution

main()
