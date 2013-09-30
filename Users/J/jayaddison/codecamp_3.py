from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def scrape_url(url):

    download = urlopen(url)
    raw = download.read()
    
    html = fromstring(raw)
    tables = html.cssselect('table')
    
    for row in tables[2].cssselect('tr')[1:]:
    
        cells = row.cssselect('td')
        items = [td.text_content() for td in cells]
        data = dict(zip(COLUMN_NAMES, items))
    
        # cleanup workers
        data['num_workers'] = int(data['num_workers'])
    
        # cleanup state
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        else:
            raise ValueError('State not found')
    
        # cleanup date
        expiration_date = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
        if expiration_date:
            data['expiration_date'] = expiration_date
    
        # cleanup pdf link
        links = cells[1].cssselect('a')
        if len(links) == 1:
            data['pdf'] = links[0].attrib['href']
    
        save([], data)

scrape_url('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def scrape_url(url):

    download = urlopen(url)
    raw = download.read()
    
    html = fromstring(raw)
    tables = html.cssselect('table')
    
    for row in tables[2].cssselect('tr')[1:]:
    
        cells = row.cssselect('td')
        items = [td.text_content() for td in cells]
        data = dict(zip(COLUMN_NAMES, items))
    
        # cleanup workers
        data['num_workers'] = int(data['num_workers'])
    
        # cleanup state
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        else:
            raise ValueError('State not found')
    
        # cleanup date
        expiration_date = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
        if expiration_date:
            data['expiration_date'] = expiration_date
    
        # cleanup pdf link
        links = cells[1].cssselect('a')
        if len(links) == 1:
            data['pdf'] = links[0].attrib['href']
    
        save([], data)

scrape_url('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')