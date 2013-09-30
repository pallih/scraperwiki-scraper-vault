###############################################################################
# Basic scraper index 01 = propertywala
###############################################################################

import scraperwiki
import datetime
import re
import time
from BeautifulSoup import BeautifulSoup

def makeTime(text):
    token = text.split()
    if token[1] == 'days':
        return long( time.time() - int(token[0])*1000*60*60*24)
    return long( time.time())


def scrape_page(city,page_url):    
    html = scraperwiki.scrape(page_url)
# get all the pages and loop through them
    soup = BeautifulSoup(html)
    #print html
    recs = soup.findAll('table',{'class':'table_list '})    # Fetch all houses from delhi 
    locTemplate = re.compile(r"^[0-9a-zA-Z/ ]+in (?P<location>[0-9a-zA-Z- ]*),*")
    recTemplate = re.compile(r"^Monthly Rent:(?P<price>[0-9,]+)Bedroom:(?P<beds>\d)[0-9a-zA-Z: ]*Posted:(?P<date_posted>[0-9a-zA-z ]+)Type:(?P<type>[0-9a-zA-z/ ]+)Area:*")
    
    for rec in recs:
        try:
            #print rec
            record = {'id':None, 'city':city, 'date_scraped':None,'date_posted': None,'location':None ,'type':None, 'beds':None,  'price':None, 'owner': None, 'number': None, 'desc':None,}   
            
            

            #match the regular expression
            result = recTemplate.match(rec.find('td',{'class':'searchList'}).text)
            locResult = locTemplate.match(rec.find('a',{'title':'Click here to view Details and contact owner.'}).text)

            record['id'] =  rec.find('input',{'type':'checkbox'})['value']
            record['city'] =  city
            record['date_scraped'] = long(time.time())
            record['date_posted'] = makeTime(result.group('date_posted'))
            record['location'] = locResult.group('location')
            record['type'] = result.group('type').replace(' / Flat','')
            record['beds'] = result.group('beds') + " Bedroom"
            record['price'] = result.group('price').replace(',','')
            record['owner'] = 'NA'
            record['number'] = 'NA'
            record['desc'] = (rec.find('td',{'class':'td_listingbold'})).text 


            #print record['location']
            scraperwiki.sqlite.save(unique_keys=['id'], data=record)
        except Exception as inst:
           #print '-------------------------------------------------------' 
           print inst
           #print 'post dropped under exceptional circumstances'
           #print rec
           #print '-------------------------------------------------------'
           pass


def scrape_site(city,url):
    scrape_page(city,url+'/page-2')
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    #print html
    #lastPageLink = soup.find('a',{'title':'Go to Last Page'}).get('href')
    #lastPageNo = int(lastPageLink[lastPageLink.rfind('-')+1:])
    #print lastPageNo
    #for i in range(1,lastPageNo+1):
    #    print url+'/page-'+str(i)
    #    scrape_page('Delhi',url+'/page-'+str(i))









# Delhi
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-new_delhi'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-faridabad_haryana'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-greater_noida_uttar_pradesh'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-noida_uttar_pradesh'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-gurgaon_haryana'
scrape_site('Delhi',starting_url)

# Mumbai
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-mumbai_maharashtra'
scrape_site('Mumbai',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-navi_mumbai_maharashtra'
scrape_site('Mumbai',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-thane_maharashtra'
scrape_site('Mumbai',starting_url)

# Others
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-bangalore_karnataka'
scrape_site('Bangalore',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-hyderabad_andhra_pradesh'
scrape_site('Hyderabad',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-pune_maharashtra'
scrape_site('Pune',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-kolkata_west_bengal'
scrape_site('Kolkata',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-chennai_tamil_nadu'
scrape_site('Chennai',starting_url)
###############################################################################
# Basic scraper index 01 = propertywala
###############################################################################

import scraperwiki
import datetime
import re
import time
from BeautifulSoup import BeautifulSoup

def makeTime(text):
    token = text.split()
    if token[1] == 'days':
        return long( time.time() - int(token[0])*1000*60*60*24)
    return long( time.time())


def scrape_page(city,page_url):    
    html = scraperwiki.scrape(page_url)
# get all the pages and loop through them
    soup = BeautifulSoup(html)
    #print html
    recs = soup.findAll('table',{'class':'table_list '})    # Fetch all houses from delhi 
    locTemplate = re.compile(r"^[0-9a-zA-Z/ ]+in (?P<location>[0-9a-zA-Z- ]*),*")
    recTemplate = re.compile(r"^Monthly Rent:(?P<price>[0-9,]+)Bedroom:(?P<beds>\d)[0-9a-zA-Z: ]*Posted:(?P<date_posted>[0-9a-zA-z ]+)Type:(?P<type>[0-9a-zA-z/ ]+)Area:*")
    
    for rec in recs:
        try:
            #print rec
            record = {'id':None, 'city':city, 'date_scraped':None,'date_posted': None,'location':None ,'type':None, 'beds':None,  'price':None, 'owner': None, 'number': None, 'desc':None,}   
            
            

            #match the regular expression
            result = recTemplate.match(rec.find('td',{'class':'searchList'}).text)
            locResult = locTemplate.match(rec.find('a',{'title':'Click here to view Details and contact owner.'}).text)

            record['id'] =  rec.find('input',{'type':'checkbox'})['value']
            record['city'] =  city
            record['date_scraped'] = long(time.time())
            record['date_posted'] = makeTime(result.group('date_posted'))
            record['location'] = locResult.group('location')
            record['type'] = result.group('type').replace(' / Flat','')
            record['beds'] = result.group('beds') + " Bedroom"
            record['price'] = result.group('price').replace(',','')
            record['owner'] = 'NA'
            record['number'] = 'NA'
            record['desc'] = (rec.find('td',{'class':'td_listingbold'})).text 


            #print record['location']
            scraperwiki.sqlite.save(unique_keys=['id'], data=record)
        except Exception as inst:
           #print '-------------------------------------------------------' 
           print inst
           #print 'post dropped under exceptional circumstances'
           #print rec
           #print '-------------------------------------------------------'
           pass


def scrape_site(city,url):
    scrape_page(city,url+'/page-2')
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    #print html
    #lastPageLink = soup.find('a',{'title':'Go to Last Page'}).get('href')
    #lastPageNo = int(lastPageLink[lastPageLink.rfind('-')+1:])
    #print lastPageNo
    #for i in range(1,lastPageNo+1):
    #    print url+'/page-'+str(i)
    #    scrape_page('Delhi',url+'/page-'+str(i))









# Delhi
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-new_delhi'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-faridabad_haryana'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-greater_noida_uttar_pradesh'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-noida_uttar_pradesh'
scrape_site('Delhi',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-gurgaon_haryana'
scrape_site('Delhi',starting_url)

# Mumbai
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-mumbai_maharashtra'
scrape_site('Mumbai',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-navi_mumbai_maharashtra'
scrape_site('Mumbai',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-thane_maharashtra'
scrape_site('Mumbai',starting_url)

# Others
starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-bangalore_karnataka'
scrape_site('Bangalore',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-hyderabad_andhra_pradesh'
scrape_site('Hyderabad',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-pune_maharashtra'
scrape_site('Pune',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-kolkata_west_bengal'
scrape_site('Kolkata',starting_url)

starting_url = 'http://www.propertywala.com/properties/type-residential/for-rent/location-chennai_tamil_nadu'
scrape_site('Chennai',starting_url)
