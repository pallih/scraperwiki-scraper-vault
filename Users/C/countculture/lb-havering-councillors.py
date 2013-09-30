import scraperwiki
import BeautifulSoup
import re

from scraperwiki import datastore

# Getting names and URLs of London Borough of Havering councillors #

#scrape page
html = scraperwiki.scrape('http://www.havering.gov.uk/index.aspx?articleid=627')
page = BeautifulSoup.BeautifulSoup(html)

#get list of wards
for ward_link in page.find(id='lhscol').findAll('a', title=re.compile("Ward")):
    ward_page = BeautifulSoup.BeautifulSoup(scraperwiki.scrape(ward_link['href']))
    #get councillors for each ward
    for councillor_link in ward_page.find(id='lhscol').findAll('a', title=re.compile("Councillor ")):
        url = councillor_link['href']
        full_name = councillor_link.string
        uid = re.search(r'id=(\d+)', url).group(1)
        #print full_name, url, uid
        
        #save to datastore
        data = {'full_name' : full_name, 'url' : url, 'uid' : uid,}
        datastore.save(unique_keys=['uid'], data=data)


import scraperwiki
import BeautifulSoup
import re

from scraperwiki import datastore

# Getting names and URLs of London Borough of Havering councillors #

#scrape page
html = scraperwiki.scrape('http://www.havering.gov.uk/index.aspx?articleid=627')
page = BeautifulSoup.BeautifulSoup(html)

#get list of wards
for ward_link in page.find(id='lhscol').findAll('a', title=re.compile("Ward")):
    ward_page = BeautifulSoup.BeautifulSoup(scraperwiki.scrape(ward_link['href']))
    #get councillors for each ward
    for councillor_link in ward_page.find(id='lhscol').findAll('a', title=re.compile("Councillor ")):
        url = councillor_link['href']
        full_name = councillor_link.string
        uid = re.search(r'id=(\d+)', url).group(1)
        #print full_name, url, uid
        
        #save to datastore
        data = {'full_name' : full_name, 'url' : url, 'uid' : uid,}
        datastore.save(unique_keys=['uid'], data=data)


