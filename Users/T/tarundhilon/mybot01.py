###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import datetime
from BeautifulSoup import BeautifulSoup

def scrape_post(city,starting_url):
    
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    debug = 'false'
    #print html
    #recs = soup.findAll('div',{'class':'tuplefr'})    # Fetch all houses from delhi 
    recs = soup.findAll('div',{'class':'sT '})    # Fetch all houses from delhi 
    for rec in recs:
        try:
            if(debug == 'true'): print rec
            record = {'city':city, 'date_scraped':None,'id':None,'location':None ,'date': None,'owner': None, 'number': None, 'desc':None, 'price':None,'type':None}   
            
            record['date_scraped'] = datetime.datetime.now()
            
            record['id'] =  rec.find('input',{'name':'propid[]'})['value']
            if(debug == 'true'): print record ['id']
            
            record['date'] = (rec.find('i',{'class':'pdate'})).string.replace(',',';')
            if(debug == 'true'): print record ['date']            

            record['owner'] =  (rec.find('input',{'name':'nm[]','type':'hidden'})['value']).capitalize()
            if(debug == 'true'): print record ['owner']            

            record['number'] =  rec.find('input',{'name':'mob[]','type':'hidden'})['value']
            if(debug == 'true'): print record ['number']            

            desRec = (rec.find('div',{'class':'sT_disc grey'}))
            record['desc'] = desRec.find('p').text 
            #record['desc'] = (rec.find('div',{'class':'sT_disc grey'})).text.replace(',',';') 
            if(debug == 'true'): print record ['desc']            

            record['price'] = (rec.find('i',{'id':'rs_'+record['id']})).text
            if(debug == 'true'): print record ['price']            

            longLocText = (rec.find('a',{'class':'f14 uline '})).text
            sIndex = longLocText.find('in') + 3
            lIndex = len(longLocText)
            record['location'] = longLocText[sIndex:lIndex]
            if(debug == 'true'): print record ['location']            

            title  = (rec.find('a',{'id':'desc_'+record['id']})['title'])
            record['type'] = title[0:title.find(',')]
            if(debug == 'true'): print record ['type']            

            if(debug == 'true'): print record
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

