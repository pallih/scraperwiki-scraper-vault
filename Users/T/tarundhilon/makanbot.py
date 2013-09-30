###############################################################################
# Basic scraper - makan
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html
    #recs = soup.findAll('div',{'class':'bbcontenth'})    # Fetch all houses from delhi 
    recs = soup.findAll('div',{'id':'search_result_box'})
    for rec in recs:
        try:
            #print rec
            record = {'city':city, 'date_scraped':None,'id':None,'location':None ,'date': None,'owner': None, 'number': None, 'desc':None, 'price':None,'type':None}   
            
            record['date_scraped'] = datetime.datetime.now()
            #print record['date_scraped']
            #<input type='checkbox' name='checkbox[]' id='checkbox[]' value='1030792'
            record['id'] =  rec.find('input',{'name':'checkbox[]'})['value']
            #print record['id']
            date = (rec.find('div',{'class':'propdate'})).find('a').text
            record['date'] = date.replace('\' ',';') 
            #print record['date']
            # <div class='contactname' style=''><b>Contact Name:</b> Rakesh&nbsp;(Agent)</div>
            owner =  rec.find('div',{'class':'contactname'}).text
            record['owner'] = owner[len('Contact Name:'):owner.find('&nbsp;')]
            #print record['owner']
            #<div class='contactnum'>
            record['number'] = ((rec.find('div',{'class':'contactnum'})).text).replace("&nbsp;","").replace("91-","")
            #print record['number']

            #<div class='desc'>Independent
            record['desc'] = (rec.find('div',{'class':'desc'})).text
            #print record['desc']
            #<div class='price'
            price = (rec.find('div',{'class':'price'})).text
            record['price'] = price[3:price.find("/-")]
            #print record['price']

            loc = (rec.find('div',{'class':'typefor'})).find('a').text   
            record['location'] = loc[loc.find('in')+3:loc.find(',')]
            #print record['location']
            #title  = (rec.find('a',{'id':'desc_'+record['id']})['title'])

            type = ((rec.find('span',{'id':'bedroom'})).text.replace('&nbsp;',' '))   
            record['type'] = ((rec.find('span',{'id':'bedroom'})).text.replace('&nbsp;',' ')).replace('s','')
            print record
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


starting_url ='http://www.makaan.com/search/search-property.php?searched=1&main=1&property_for=2&property_type=1&city=M1&budget_from=5000&budget_to=50000&pb%5B%5D=1'
scrape_post('Delhi',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=12&preference=R&class[]=O'
#scrape_post('Mumbai',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=32&preference=R&class[]=O'
#scrape_post('Chennai',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=38&preference=R&class[]=O'
#scrape_post('Hyderabad',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=19&preference=R&class[]=O'
#scrape_post('Pune',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=20&preference=R&class[]=O'
#scrape_post('Bangalore',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=25&preference=R&class[]=O'
#scrape_post('Kolkata',starting_url)

###############################################################################
# Basic scraper - makan
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    print html
    #recs = soup.findAll('div',{'class':'bbcontenth'})    # Fetch all houses from delhi 
    recs = soup.findAll('div',{'id':'search_result_box'})
    for rec in recs:
        try:
            #print rec
            record = {'city':city, 'date_scraped':None,'id':None,'location':None ,'date': None,'owner': None, 'number': None, 'desc':None, 'price':None,'type':None}   
            
            record['date_scraped'] = datetime.datetime.now()
            #print record['date_scraped']
            #<input type='checkbox' name='checkbox[]' id='checkbox[]' value='1030792'
            record['id'] =  rec.find('input',{'name':'checkbox[]'})['value']
            #print record['id']
            date = (rec.find('div',{'class':'propdate'})).find('a').text
            record['date'] = date.replace('\' ',';') 
            #print record['date']
            # <div class='contactname' style=''><b>Contact Name:</b> Rakesh&nbsp;(Agent)</div>
            owner =  rec.find('div',{'class':'contactname'}).text
            record['owner'] = owner[len('Contact Name:'):owner.find('&nbsp;')]
            #print record['owner']
            #<div class='contactnum'>
            record['number'] = ((rec.find('div',{'class':'contactnum'})).text).replace("&nbsp;","").replace("91-","")
            #print record['number']

            #<div class='desc'>Independent
            record['desc'] = (rec.find('div',{'class':'desc'})).text
            #print record['desc']
            #<div class='price'
            price = (rec.find('div',{'class':'price'})).text
            record['price'] = price[3:price.find("/-")]
            #print record['price']

            loc = (rec.find('div',{'class':'typefor'})).find('a').text   
            record['location'] = loc[loc.find('in')+3:loc.find(',')]
            #print record['location']
            #title  = (rec.find('a',{'id':'desc_'+record['id']})['title'])

            type = ((rec.find('span',{'id':'bedroom'})).text.replace('&nbsp;',' '))   
            record['type'] = ((rec.find('span',{'id':'bedroom'})).text.replace('&nbsp;',' ')).replace('s','')
            print record
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


starting_url ='http://www.makaan.com/search/search-property.php?searched=1&main=1&property_for=2&property_type=1&city=M1&budget_from=5000&budget_to=50000&pb%5B%5D=1'
scrape_post('Delhi',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=12&preference=R&class[]=O'
#scrape_post('Mumbai',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=32&preference=R&class[]=O'
#scrape_post('Chennai',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=38&preference=R&class[]=O'
#scrape_post('Hyderabad',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=19&preference=R&class[]=O'
#scrape_post('Pune',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=20&preference=R&class[]=O'
#scrape_post('Bangalore',starting_url)

#starting_url = 'http://www.99acres.com/do/quicksearch/search?search_type=QS&search_location=SH&city=25&preference=R&class[]=O'
#scrape_post('Kolkata',starting_url)

