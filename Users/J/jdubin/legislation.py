# Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retireive a page
keys = range(73, 78)
starting_url = 'http://legislation.phila.gov/detailreport/?key='

def scrape_legis_file(key, soup):
    ltype = ''
    lstatus = ''

    span = soup.find('span', {'id':'lblFileTypeValue'})
    ltype = span.text

    span = soup.find('span', {'id':'lblFileStatusValue'})
    ltype = span.text

    record = {
    'key' : key,
    'type' : ltype,
    'status' : lstatus,
    }

    print record
    return record
    

def is_error_page(soup):
    error_p = soup.find('p', 'errorText')
    
    if error_p is None: return False
    else: return True

def get_latest_key():
    max = 95
    for elem in scraperwiki.datastore.getData('philadelphia_legislative_files'):
        max = elem['key'] if elem['key'] > max else max
    return int(max)


last_key = get_latest_key()
curr_key = last_key + 5
while True:
    html = scraperwiki.scrape(starting_url + str(curr_key))
    soup = BeautifulSoup(html)


    if is_error_page(soup):
        break

    record = scrape_legis_file(curr_key, soup)
    scraperwiki.datastore.save(['key'], record)
    scraperwiki.datastore.getData('philadelphia_legislative_files')
    curr_key = curr_key + 1
    # Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retireive a page
keys = range(73, 78)
starting_url = 'http://legislation.phila.gov/detailreport/?key='

def scrape_legis_file(key, soup):
    ltype = ''
    lstatus = ''

    span = soup.find('span', {'id':'lblFileTypeValue'})
    ltype = span.text

    span = soup.find('span', {'id':'lblFileStatusValue'})
    ltype = span.text

    record = {
    'key' : key,
    'type' : ltype,
    'status' : lstatus,
    }

    print record
    return record
    

def is_error_page(soup):
    error_p = soup.find('p', 'errorText')
    
    if error_p is None: return False
    else: return True

def get_latest_key():
    max = 95
    for elem in scraperwiki.datastore.getData('philadelphia_legislative_files'):
        max = elem['key'] if elem['key'] > max else max
    return int(max)


last_key = get_latest_key()
curr_key = last_key + 5
while True:
    html = scraperwiki.scrape(starting_url + str(curr_key))
    soup = BeautifulSoup(html)


    if is_error_page(soup):
        break

    record = scrape_legis_file(curr_key, soup)
    scraperwiki.datastore.save(['key'], record)
    scraperwiki.datastore.getData('philadelphia_legislative_files')
    curr_key = curr_key + 1
    