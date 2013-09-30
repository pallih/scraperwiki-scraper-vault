'''Follows pages on Rwanda Microfinance Web Portal'''

import BeautifulSoup
import requests
#import json
import re
from scraperwiki.sqlite import save
from time import time
DATE = time()

base = 'http://www.rwandamicrofinance.org/'

def getKind(td, label, replace=""):
    try:
        return td.findAll('span', attrs={'class':label})[0].text
    except IndexError:
        return ''

def eachpage(url, kind):
    _d = requests.get(base+url)
    d = BeautifulSoup.BeautifulSoup(_d.content)
    result = []
    for td in d.findAll('td', attrs={'style': re.compile('.*green.gif.*')}):
        out = {}
        out['name'] = td.findAll('p')[0].text
        out['place'] = getKind(td, 'sobi2Listing_field_place')
        out['email'] = getKind(td, 
            'sobi2Listing_field_email').replace('Email:','')
        out['contact_person'] = getKind(td,
            'sobi2Listing_field_contact_person').replace('Contact Person:','')
        out['phone'] = getKind(td,
            'sobi2Listing_field_phone').replace('Phone:','')
        out['type'] = kind
        if kind == "MFI":
            out['standardtype'] = 'Microenterprise Lenders'
        elif kind == 'Unions':
            out['standardtype'] = 'Cooperatives'
        else:
            out['standardtype'] = 'Other credit providers'
        result.append(out)
        
    n = d.findAll('a', attrs={'title':'Next'})
    try:
        n = n[0].attrs[1][1]
    except:
        n = None
    return result,n

def main():
    out = []
    #outfile = open('rwandamicrofinance.json','w')
    kinds = {('7','123'): 'MFI', ('8','124'): 'Unions', ('9','125'): 'SARL', ('10','126'): 'SA'}
    for (k1,k2),v in kinds.iteritems():
        start = 'index.php?option=com_sobi2&catid=%s&Itemid=%s&lang=en'%(k1,k2)
        result, n = eachpage(start, v)
        out.extend(result)
        while n!=None:
            result,n = eachpage(n, v)
            out.extend(result)
    for row in out:
        row['date_scraped'] = DATE
    save([], out)
    #json.dump(out, outfile)

main()'''Follows pages on Rwanda Microfinance Web Portal'''

import BeautifulSoup
import requests
#import json
import re
from scraperwiki.sqlite import save
from time import time
DATE = time()

base = 'http://www.rwandamicrofinance.org/'

def getKind(td, label, replace=""):
    try:
        return td.findAll('span', attrs={'class':label})[0].text
    except IndexError:
        return ''

def eachpage(url, kind):
    _d = requests.get(base+url)
    d = BeautifulSoup.BeautifulSoup(_d.content)
    result = []
    for td in d.findAll('td', attrs={'style': re.compile('.*green.gif.*')}):
        out = {}
        out['name'] = td.findAll('p')[0].text
        out['place'] = getKind(td, 'sobi2Listing_field_place')
        out['email'] = getKind(td, 
            'sobi2Listing_field_email').replace('Email:','')
        out['contact_person'] = getKind(td,
            'sobi2Listing_field_contact_person').replace('Contact Person:','')
        out['phone'] = getKind(td,
            'sobi2Listing_field_phone').replace('Phone:','')
        out['type'] = kind
        if kind == "MFI":
            out['standardtype'] = 'Microenterprise Lenders'
        elif kind == 'Unions':
            out['standardtype'] = 'Cooperatives'
        else:
            out['standardtype'] = 'Other credit providers'
        result.append(out)
        
    n = d.findAll('a', attrs={'title':'Next'})
    try:
        n = n[0].attrs[1][1]
    except:
        n = None
    return result,n

def main():
    out = []
    #outfile = open('rwandamicrofinance.json','w')
    kinds = {('7','123'): 'MFI', ('8','124'): 'Unions', ('9','125'): 'SARL', ('10','126'): 'SA'}
    for (k1,k2),v in kinds.iteritems():
        start = 'index.php?option=com_sobi2&catid=%s&Itemid=%s&lang=en'%(k1,k2)
        result, n = eachpage(start, v)
        out.extend(result)
        while n!=None:
            result,n = eachpage(n, v)
            out.extend(result)
    for row in out:
        row['date_scraped'] = DATE
    save([], out)
    #json.dump(out, outfile)

main()