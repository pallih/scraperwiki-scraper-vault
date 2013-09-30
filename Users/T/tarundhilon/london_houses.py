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
  #  print html
    recs = soup.findAll('div',{'class':'summarymaincontent'}) 
    for rec in recs:
        #print rec
        record = {'id':None, 'date_scraped':None,'location':None , 'beds':None,  'price':None, 'owner': None, 'url': None} 

        record['id'] = rec.find('a',{'class':'photo'})['id'].replace("prop","")
        record['date_scraped'] = time.time()
        record['location'] = rec.find('span',{'class':'displayaddress'}).text 
        record['beds'] = rec.find('a',{'id':'standardPropertySummary'+record['id']}).find('span',{'class':''}).text
        record['price'] = rec.find('p',{'class':'price'}).text.replace("&pound;","") 
        record['owner'] = rec.find('p',{'class':'branchblurb'}).text 
        record['url'] = "http://www.rightmove.co.uk" + rec.find('a',{'id':'standardPropertySummary'+record['id']})['href'] 
        scraperwiki.sqlite.save(unique_keys=['id'], data=record)

    divs = soup.findAll('a',{'class':'pagenavigation active'})
    for div in divs:
        if div.text == "next":
            scrape_page(city,"http://www.rightmove.co.uk" +div['href'])










# Delhi
#starting_url = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E85443&insId=2&radius=1.0&maxPrice=259000'

starting_url = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E93977&insId=2&radius=1.0&minBedrooms=2&maxPrice=330000'
# queens park REGION^87527
# maida vale REGION%5E85443
# wandsworth 93977
scrape_page('Maida Vale',starting_url)














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
  #  print html
    recs = soup.findAll('div',{'class':'summarymaincontent'}) 
    for rec in recs:
        #print rec
        record = {'id':None, 'date_scraped':None,'location':None , 'beds':None,  'price':None, 'owner': None, 'url': None} 

        record['id'] = rec.find('a',{'class':'photo'})['id'].replace("prop","")
        record['date_scraped'] = time.time()
        record['location'] = rec.find('span',{'class':'displayaddress'}).text 
        record['beds'] = rec.find('a',{'id':'standardPropertySummary'+record['id']}).find('span',{'class':''}).text
        record['price'] = rec.find('p',{'class':'price'}).text.replace("&pound;","") 
        record['owner'] = rec.find('p',{'class':'branchblurb'}).text 
        record['url'] = "http://www.rightmove.co.uk" + rec.find('a',{'id':'standardPropertySummary'+record['id']})['href'] 
        scraperwiki.sqlite.save(unique_keys=['id'], data=record)

    divs = soup.findAll('a',{'class':'pagenavigation active'})
    for div in divs:
        if div.text == "next":
            scrape_page(city,"http://www.rightmove.co.uk" +div['href'])










# Delhi
#starting_url = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E85443&insId=2&radius=1.0&maxPrice=259000'

starting_url = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E93977&insId=2&radius=1.0&minBedrooms=2&maxPrice=330000'
# queens park REGION^87527
# maida vale REGION%5E85443
# wandsworth 93977
scrape_page('Maida Vale',starting_url)














