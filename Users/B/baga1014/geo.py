###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
#import lxml.html
#import urlparse


# retrieve a page
starting_url = 'http://earthquake.usgs.gov/earthquakes/recenteqsww/Quakes/quakes_big.php'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)



def scrape_link(url):
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    record = {}
    data = soup.findAll('td')
    if data:
        record['Magnitude'] = data[0].text
        record['Date-Time'] = data[1].text
        record['Location'] = data[2].text    
        record['Depth'] = data[3].text
        record['Region'] = data[4].text
        record['Distances'] = data[5].text
        record['Uncertainty'] = data[6].text
        record['Parameter'] = data[7].text
        record['Source'] = data[8].text
        record['Event-ID'] = data[9].text
        scraperwiki.datastore.save(['Date-Time'],record)
        print record


# use BeautifulSoup to get all <td> tags

base_url='http://earthquake.usgs.gov'
tds = soup.findAll('td')
r=''

for td in tds:
    
    tmp = td.text.replace('&nbsp;','')
    
    if td.text=='MAP':
        r = ''   
        count =0
    count +=1 
    r = r+ tmp +'|'
    if count ==3:
        print base_url+td.a.get('href')
        scrape_link(base_url+td.a.get('href')) 
    
    if count ==7:
        print r
        count =0                        
    
        record = { "td" : r }
        #save records to the datastore
        #scraperwiki.datastore.save(["td"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
#import lxml.html
#import urlparse


# retrieve a page
starting_url = 'http://earthquake.usgs.gov/earthquakes/recenteqsww/Quakes/quakes_big.php'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)



def scrape_link(url):
    html = scraperwiki.scrape(url)
    print html
    soup = BeautifulSoup(html)
    record = {}
    data = soup.findAll('td')
    if data:
        record['Magnitude'] = data[0].text
        record['Date-Time'] = data[1].text
        record['Location'] = data[2].text    
        record['Depth'] = data[3].text
        record['Region'] = data[4].text
        record['Distances'] = data[5].text
        record['Uncertainty'] = data[6].text
        record['Parameter'] = data[7].text
        record['Source'] = data[8].text
        record['Event-ID'] = data[9].text
        scraperwiki.datastore.save(['Date-Time'],record)
        print record


# use BeautifulSoup to get all <td> tags

base_url='http://earthquake.usgs.gov'
tds = soup.findAll('td')
r=''

for td in tds:
    
    tmp = td.text.replace('&nbsp;','')
    
    if td.text=='MAP':
        r = ''   
        count =0
    count +=1 
    r = r+ tmp +'|'
    if count ==3:
        print base_url+td.a.get('href')
        scrape_link(base_url+td.a.get('href')) 
    
    if count ==7:
        print r
        count =0                        
    
        record = { "td" : r }
        #save records to the datastore
        #scraperwiki.datastore.save(["td"], record) 
    