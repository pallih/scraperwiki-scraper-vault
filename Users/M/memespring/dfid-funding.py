import scraperwiki
import BeautifulSoup

from scraperwiki import datastore
from datetime import datetime


def parse_page(page):


    wrapper = page.find('div', {'id': 'print_div1'})
    for row in wrapper.findAll('tr')[1:]:
        cells = row.findAll('td')
        title = cells[0].contents[0].string
        country = cells[1].string
        funding_type = cells[2].string
        stage = cells[3].string
        start_date = datetime.strptime(cells[4].string, "%d/%m/%Y")
        total_budget = cells[5].string.replace(',', '')
    
    
        data = { 'title' : title, 'country' : country, 'funding_type': funding_type, 'stage': stage, 'total_budget': total_budget, 'start_date': start_date}
        datastore.save(unique_keys=['title','country', 'total_budget', 'start_date'], data=data, date=start_date)
    
    
def run_scraper(start_url):
    
    print "Starting next page"
    
    #scrape page and parse it
    html = scraperwiki.scrape(start_url)
    page = BeautifulSoup.BeautifulSoup(html)
    parse_page(page)


    #find the next page and call this function again
    next_image = page.find('img', {'src': 'images/rightnav.gif'})
    if next_image:
       run_scraper('http://projects.dfid.gov.uk/' + next_image.parent['href'])


run_scraper('http://projects.dfid.gov.uk/SearchResults.asp?RecordsPerPage=100&PageNo=1')

import scraperwiki
import BeautifulSoup

from scraperwiki import datastore
from datetime import datetime


def parse_page(page):


    wrapper = page.find('div', {'id': 'print_div1'})
    for row in wrapper.findAll('tr')[1:]:
        cells = row.findAll('td')
        title = cells[0].contents[0].string
        country = cells[1].string
        funding_type = cells[2].string
        stage = cells[3].string
        start_date = datetime.strptime(cells[4].string, "%d/%m/%Y")
        total_budget = cells[5].string.replace(',', '')
    
    
        data = { 'title' : title, 'country' : country, 'funding_type': funding_type, 'stage': stage, 'total_budget': total_budget, 'start_date': start_date}
        datastore.save(unique_keys=['title','country', 'total_budget', 'start_date'], data=data, date=start_date)
    
    
def run_scraper(start_url):
    
    print "Starting next page"
    
    #scrape page and parse it
    html = scraperwiki.scrape(start_url)
    page = BeautifulSoup.BeautifulSoup(html)
    parse_page(page)


    #find the next page and call this function again
    next_image = page.find('img', {'src': 'images/rightnav.gif'})
    if next_image:
       run_scraper('http://projects.dfid.gov.uk/' + next_image.parent['href'])


run_scraper('http://projects.dfid.gov.uk/SearchResults.asp?RecordsPerPage=100&PageNo=1')

