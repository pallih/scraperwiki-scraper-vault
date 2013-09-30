###############################################################################
# Boston Eating Establishment Temporary Permit Suspensions
# for the last 365 days
# 
# Fields:
#   establishment
#   address
#   suspended_date
#   suspended_url
#   reinstated_date
#   reinstated_url
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date,datetime

# retrieve a page
starting_url = 'http://www.cityofboston.gov/isd/health/tsop.asp'
html = scraperwiki.scrape(starting_url, {'cboperiod':'2000'})# Form pulldown has 30,60,90 days, but we can use whatever number we want
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div',{'class':'mainLeadStory'})# IDs the central part of scrape
susp_rows = div.findAll('tr')

def absolutize_url(url):
    if url[0] == '/':
        url = 'http://www.cityofboston.gov' + url#what is going on here?
    elif url[:4] != 'http':
        url = 'http://www.cityofboston.gov/isd/health/' + url
    
    return url

def isoformat(d):
    ''' Convert US style mm/dd/yyyy date to ISO format'''
    try:
        return datetime.strptime(d,'%m/%d/%Y').strftime('%Y-%m-%d')
    except:
        return d

for susp_row in susp_rows[1:]:## Skip first row containing headings
    establishment = ''
    address = ''
    susp_date = ''
    susp_url = ''
    reinst_date = ''
    reinst_url = ''
    
    cells = susp_row.findAll('td')
    
    establishment = cells[0].text
    address = cells[1].text
    susp_date = isoformat(cells[2].text)
    reinst_date = isoformat(cells[3].text) # This actually contains the most recent reinstatement, not the one which matches the suspension
    
    susp_a = cells[2].find('a')
    if susp_a:
        susp_url = absolutize_url(susp_a['href'])
    
    reinst_a = cells[3].find('a')
    if reinst_a:
        reinst_url = absolutize_url(reinst_a['href'])
    
    record = { 
        'date_scraped': date.today().isoformat(),
        'establishment' : establishment,
        'address' : address,
        'suspended_date' : susp_date,
        'suspended_url' : susp_url,
        'reinstated_date' : reinst_date,
        'reinstated_url' : reinst_url
    }
    
    print record
    
    scraperwiki.sqlite.save(['establishment','suspended_date'], record, verbose=2)

###############################################################################
# Boston Eating Establishment Temporary Permit Suspensions
# for the last 365 days
# 
# Fields:
#   establishment
#   address
#   suspended_date
#   suspended_url
#   reinstated_date
#   reinstated_url
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date,datetime

# retrieve a page
starting_url = 'http://www.cityofboston.gov/isd/health/tsop.asp'
html = scraperwiki.scrape(starting_url, {'cboperiod':'2000'})# Form pulldown has 30,60,90 days, but we can use whatever number we want
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div',{'class':'mainLeadStory'})# IDs the central part of scrape
susp_rows = div.findAll('tr')

def absolutize_url(url):
    if url[0] == '/':
        url = 'http://www.cityofboston.gov' + url#what is going on here?
    elif url[:4] != 'http':
        url = 'http://www.cityofboston.gov/isd/health/' + url
    
    return url

def isoformat(d):
    ''' Convert US style mm/dd/yyyy date to ISO format'''
    try:
        return datetime.strptime(d,'%m/%d/%Y').strftime('%Y-%m-%d')
    except:
        return d

for susp_row in susp_rows[1:]:## Skip first row containing headings
    establishment = ''
    address = ''
    susp_date = ''
    susp_url = ''
    reinst_date = ''
    reinst_url = ''
    
    cells = susp_row.findAll('td')
    
    establishment = cells[0].text
    address = cells[1].text
    susp_date = isoformat(cells[2].text)
    reinst_date = isoformat(cells[3].text) # This actually contains the most recent reinstatement, not the one which matches the suspension
    
    susp_a = cells[2].find('a')
    if susp_a:
        susp_url = absolutize_url(susp_a['href'])
    
    reinst_a = cells[3].find('a')
    if reinst_a:
        reinst_url = absolutize_url(reinst_a['href'])
    
    record = { 
        'date_scraped': date.today().isoformat(),
        'establishment' : establishment,
        'address' : address,
        'suspended_date' : susp_date,
        'suspended_url' : susp_url,
        'reinstated_date' : reinst_date,
        'reinstated_url' : reinst_url
    }
    
    print record
    
    scraperwiki.sqlite.save(['establishment','suspended_date'], record, verbose=2)

