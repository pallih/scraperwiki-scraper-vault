###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html
    recs = soup.findAll('div',{'iehf':'tpS'})    # iehf="tpS" Fetch all houses from delhi 
    for rec in recs:
        try:
            print rec
            record = {'city':city, 'date_scraped':None,'id':None,'location':None ,'date': None,'owner': None, 'number': None, 'desc':None, 'price':None,'type':None}   
            
            record['date_scraped'] = datetime.datetime.now()
            print "date_scraped :" + str(record['date_scraped'])

            record['id'] =  rec.find('input',{'name':'propid[]'})['value']
            print 'id :' + record['id']

            record['date'] = rec.find('i',{'class':'pdate'}).text #<i class="pdate">May 19, 2012</i>
            print 'date :' + record['date']

            record['owner'] =  (rec.find('input',{'name':'nm[]','type':'hidden'})['value']).capitalize()
            print 'owner :' + record['owner']

            record['number'] =  rec.find('input',{'name':'mob[]','type':'hidden'})['value']
            print 'number :' + record['number']


            record['desc'] = (rec.find('div',{'class':'sT_disc grey'})).find('p').text
            print 'desc :' + record['desc']

            record['price'] = (rec.find('i',{'id':'rs_'+record['id']})).text
            print 'price :' + record['price']

            #longLocText = (rec.find('a',{'class':'f14'})).text
            longLocText = (rec.find('a',{'id':'desc_'+record['id']})).text
            #print longLocText

            sIndex = longLocText.find('in') + 3
            lIndex = len(longLocText)
            record['location'] = longLocText[sIndex:lIndex]
            print record['location']

            title  = (rec.find('a',{'id':'desc_'+record['id']})['title'])
            record['type'] = title[0:title.find(',')]
           # print record['type']

            #print record
            scraperwiki.sqlite.save(unique_keys=['id','city','owner','number','location','price'], data=record)
        except:
           print 'post dropped under exceptional circumstances'
           pass


# retrieve a page
#
#Delhi All - 1
#Bombay All - 12
#Chennai All - 32
#Hyderabad All - 38
#Pune All - 19


starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=1&preference=R&class[]=O'
scrape_post('Delhi',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=12&preference=R&class[]=O'
scrape_post('Mumbai',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=32&preference=R&class[]=O'
scrape_post('Chennai',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=38&preference=R&class[]=O'
scrape_post('Hyderabad',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=19&preference=R&class[]=O'
scrape_post('Pune',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=20&preference=R&class[]=O'
scrape_post('Bangalore',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=25&preference=R&class[]=O'
scrape_post('Kolkata',starting_url)

###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html
    recs = soup.findAll('div',{'iehf':'tpS'})    # iehf="tpS" Fetch all houses from delhi 
    for rec in recs:
        try:
            print rec
            record = {'city':city, 'date_scraped':None,'id':None,'location':None ,'date': None,'owner': None, 'number': None, 'desc':None, 'price':None,'type':None}   
            
            record['date_scraped'] = datetime.datetime.now()
            print "date_scraped :" + str(record['date_scraped'])

            record['id'] =  rec.find('input',{'name':'propid[]'})['value']
            print 'id :' + record['id']

            record['date'] = rec.find('i',{'class':'pdate'}).text #<i class="pdate">May 19, 2012</i>
            print 'date :' + record['date']

            record['owner'] =  (rec.find('input',{'name':'nm[]','type':'hidden'})['value']).capitalize()
            print 'owner :' + record['owner']

            record['number'] =  rec.find('input',{'name':'mob[]','type':'hidden'})['value']
            print 'number :' + record['number']


            record['desc'] = (rec.find('div',{'class':'sT_disc grey'})).find('p').text
            print 'desc :' + record['desc']

            record['price'] = (rec.find('i',{'id':'rs_'+record['id']})).text
            print 'price :' + record['price']

            #longLocText = (rec.find('a',{'class':'f14'})).text
            longLocText = (rec.find('a',{'id':'desc_'+record['id']})).text
            #print longLocText

            sIndex = longLocText.find('in') + 3
            lIndex = len(longLocText)
            record['location'] = longLocText[sIndex:lIndex]
            print record['location']

            title  = (rec.find('a',{'id':'desc_'+record['id']})['title'])
            record['type'] = title[0:title.find(',')]
           # print record['type']

            #print record
            scraperwiki.sqlite.save(unique_keys=['id','city','owner','number','location','price'], data=record)
        except:
           print 'post dropped under exceptional circumstances'
           pass


# retrieve a page
#
#Delhi All - 1
#Bombay All - 12
#Chennai All - 32
#Hyderabad All - 38
#Pune All - 19


starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=1&preference=R&class[]=O'
scrape_post('Delhi',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=12&preference=R&class[]=O'
scrape_post('Mumbai',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=32&preference=R&class[]=O'
scrape_post('Chennai',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=38&preference=R&class[]=O'
scrape_post('Hyderabad',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=19&preference=R&class[]=O'
scrape_post('Pune',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=20&preference=R&class[]=O'
scrape_post('Bangalore',starting_url)

starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=25&preference=R&class[]=O'
scrape_post('Kolkata',starting_url)

