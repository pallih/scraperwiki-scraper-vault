###############################################################################
# Scraper for Organisations Previously Known as Charities from the Northern Ireland Charity Commission
# http://www.charitycommissionni.org.uk/Library/ccni_files/List_of_Organisations.htm
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time
import re

# retrieve the Register of Mergers page
starting_url = 'http://www.charitycommissionni.org.uk/Library/ccni_files/List_of_Organisations.htm'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#ps = soup.findAll(style='font-size:8.0pt;font-family:Verdana') 
ps = soup.findAll('p')

for p in ps:
    spans = p.findAll(style='font-size:8.0pt;font-family:Verdana')
    if len(spans)>0:
        name = ''
        for span in spans:
            try:
                name = name + span.string
            except:
                continue
        name = name.replace('\r',' ')
        name = name.replace('\n','')
        name = name.replace('&amp;','&')
        if name=='&nbsp;':
            continue
        elif name==' ':
            continue
        elif name=='':
            continue
        elif name==None:
            continue
        else:
            record = { "name" : name }
            scraperwiki.datastore.save(["name"], record)
            print record, "- saved"

