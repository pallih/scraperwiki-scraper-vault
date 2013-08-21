###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import urllib
import re

# dox: http://www.crummy.com/software/BeautifulSoup/documentation.html

starting_url = 'http://metrix.station.ee/'
scraperwiki.metadata.save('data_columns', ['date', 'rank', 'name', 'visitors', 'change', 'localvisitors', 'newvisitors', 'bounce', 'timeonsite', 'pageviews'])
TESTING = False

#### FIND DATES
def process_all_dates(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # find week dropdown box <select name="selweek">
    selweek = soup.find('select', attrs={'name': 'selweek'})
    
    dates = [opt['value'] for opt in selweek]
    print 'dates=', dates
    if TESTING: dates = dates[:3]

    for date in dates:
        handle_pages_for_date(date)

#### FIND PAGES
def handle_pages_for_date(date):
    date_url = 'http://metrix.station.ee/?selweek=' + date
    html = scraperwiki.scrape(date_url)
    soup = BeautifulSoup(html)

    pager = soup.find('div', attrs={'id': 'pager'})
    pages = pager.findAll('a')
    if TESTING: pages = pages[:3]

    for page in pages:
        print 'Date %s: getting page %s of %s' % (date, page.text, len(pages))
        page_url = urllib.basejoin(date_url, page['href'])

        scrape_page(page_url, date)

#### FIND DATAPOINTS
def scrape_page(url, date):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    table = soup.find('table', attrs={'id': 'alltable'})
    record = {}

    for tr in table.findAll('tr'):
        row = tr.findAll('td')
        #print row
        if len(row) < 8:
            continue

        record['date']          = date
        record['rank']          = clean_int(row[0].text)
        record['name']          = row[1].text
        record['url']           = row[1].find('a')['title']
        record['visitors']      = clean_int(row[2].text)
        record['change']        = clean_float(row[3].text) # percentage
        record['localvisitors'] = clean_float(row[4].text) # percentage
        record['newvisitors']   = clean_float(row[5].text) # percentage
        record['bounce']        = clean_float(row[6].text) # percentage
        record['timeonsite']    = clean_float(row[7].text) # minutes
        record['pageviews']     = clean_int(row[8].text)

        record['key'] = (date, record['name'])
        scraperwiki.datastore.save(['key'], record)

#### FUNCTIONS
digit_re = re.compile(r'[^.0-9]+')
def clean_int(text):
    return int(digit_re.sub('', text))

def clean_float(text):
    return float(digit_re.sub('', text))

#### RUN
process_all_dates(starting_url)


