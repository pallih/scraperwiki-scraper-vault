import scraperwiki

# Blank Python
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request

# index page listing nearest 10 results
# http://www.nhs24.com/FindLocal?postcode=EH9+1PR&service=GPs
baseurl = "http://www.nhs24.com/FindLocal?service=GPs&postcode="

start_postcode = 'EH9 1PR'

def postcode_search(postcode):
    postcode = postcode.replace(' ','%20')
    html = urlopen(baseurl+postcode).read()
    
    soup = BeautifulSoup(html)
    table = soup.find('table',{'id':'tblPharm'})
    rows = table.findAll('tr')
    for row in rows:
        practise = {}
        addr = row.find('span',{'class':'captial'})
        print addr
        #name_addr = row.find('td',{'class':'tblPharmAdd'})
        
        #print name_addr

postcode_search(start_postcode)


import scraperwiki

# Blank Python
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request

# index page listing nearest 10 results
# http://www.nhs24.com/FindLocal?postcode=EH9+1PR&service=GPs
baseurl = "http://www.nhs24.com/FindLocal?service=GPs&postcode="

start_postcode = 'EH9 1PR'

def postcode_search(postcode):
    postcode = postcode.replace(' ','%20')
    html = urlopen(baseurl+postcode).read()
    
    soup = BeautifulSoup(html)
    table = soup.find('table',{'id':'tblPharm'})
    rows = table.findAll('tr')
    for row in rows:
        practise = {}
        addr = row.find('span',{'class':'captial'})
        print addr
        #name_addr = row.find('td',{'class':'tblPharmAdd'})
        
        #print name_addr

postcode_search(start_postcode)


