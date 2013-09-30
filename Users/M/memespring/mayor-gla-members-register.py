import scraperwiki
import BeautifulSoup

from scraperwiki import datastore
from datetime import datetime

        
def parse_page(page):        

    #find each row on this page
    for table in page.findAll('table', {'class': 't18Standard'}):
        for row in table.findAll('tr')[1:]: 

            #strip out the details of each gift
            person_name = row.contents[0].string
            date_as_listed = row.contents[1].string
            detail_of_gift = row.contents[2].string
            donor_of_gift = row.contents[3].string

            #convert the date to a proper datetime object
            date_of_gift = datetime.strptime(date_as_listed, "%d-%b-%y")
            
            print "Found a gift for " + person_name
            data = {'person_name': person_name, 'detail_of_gift': detail_of_gift, 'donor_of_gift': donor_of_gift, 'date_as_listed': date_as_listed}
            
        
            #save it to the datastore
            datastore.save(unique_keys = ['person_name', 'date_as_listed', 'detail_of_gift'], data = data, date=date_of_gift)

    
            

def run_scraper(url):

    #find the page
    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)

    #extract the data and save to the datastore
    parse_page(page)

    #find the next page or exit
    pagination_links = page.findAll('a', {'class': 't18pagination'})
    for pagination_link in pagination_links:
        
        #see if there is another page after this one
        next_url = False
        if pagination_links[0].string == 'Next &gt;':
            #get the url of the next page then recall this function
            next_url = 'http://www.london.gov.uk/pls/apex/' + pagination_links[0]['href']

        elif len(pagination_links) == 2 and pagination_links[1].string == 'Next &gt;':
            next_url = 'http://www.london.gov.uk/pls/apex/' + pagination_links[1]['href']            

        
        #if there are no more pages, exit the function, if there are run it again with the next url
        if next_url == False:
            return
        else:
            print 'Starting next page'
            run_scraper(next_url)
            

#Run the scraper, starting with the first page.
run_scraper('http://www.london.gov.uk/pls/apex/f?p=135:1:1645971611271101:pg_R_15919606303126599:NO&pg_min_row=0&pg_max_rows=50&pg_rows_fetched=50')


import scraperwiki
import BeautifulSoup

from scraperwiki import datastore
from datetime import datetime

        
def parse_page(page):        

    #find each row on this page
    for table in page.findAll('table', {'class': 't18Standard'}):
        for row in table.findAll('tr')[1:]: 

            #strip out the details of each gift
            person_name = row.contents[0].string
            date_as_listed = row.contents[1].string
            detail_of_gift = row.contents[2].string
            donor_of_gift = row.contents[3].string

            #convert the date to a proper datetime object
            date_of_gift = datetime.strptime(date_as_listed, "%d-%b-%y")
            
            print "Found a gift for " + person_name
            data = {'person_name': person_name, 'detail_of_gift': detail_of_gift, 'donor_of_gift': donor_of_gift, 'date_as_listed': date_as_listed}
            
        
            #save it to the datastore
            datastore.save(unique_keys = ['person_name', 'date_as_listed', 'detail_of_gift'], data = data, date=date_of_gift)

    
            

def run_scraper(url):

    #find the page
    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)

    #extract the data and save to the datastore
    parse_page(page)

    #find the next page or exit
    pagination_links = page.findAll('a', {'class': 't18pagination'})
    for pagination_link in pagination_links:
        
        #see if there is another page after this one
        next_url = False
        if pagination_links[0].string == 'Next &gt;':
            #get the url of the next page then recall this function
            next_url = 'http://www.london.gov.uk/pls/apex/' + pagination_links[0]['href']

        elif len(pagination_links) == 2 and pagination_links[1].string == 'Next &gt;':
            next_url = 'http://www.london.gov.uk/pls/apex/' + pagination_links[1]['href']            

        
        #if there are no more pages, exit the function, if there are run it again with the next url
        if next_url == False:
            return
        else:
            print 'Starting next page'
            run_scraper(next_url)
            

#Run the scraper, starting with the first page.
run_scraper('http://www.london.gov.uk/pls/apex/f?p=135:1:1645971611271101:pg_R_15919606303126599:NO&pg_min_row=0&pg_max_rows=50&pg_rows_fetched=50')


