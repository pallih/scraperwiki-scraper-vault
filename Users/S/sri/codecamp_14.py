from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

def scrape_table(url):
    download = urlopen(url)
    raw = download.read()
    
    html = fromstring(raw)
    table = html.cssselect('table')[2]
    
    for tr in table.cssselect('tr')[1:]:
        cell_text = [td.text_content() for td in tr.cssselect('td')]
        data = dict(zip(COLUMN_NAMES, cell_text))
        data['num_workers'] = int(data['num_workers'])
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        data['expiration_date'] = datetime.datetime.strptime(
            data['expiration_date'],
            '%m-%d-%y'
        ).date()
    
        a_elements = tr.cssselect('a')
        if len(a_elements) > 1:
            raise ValueError('Row has multiple a tags.')
        elif len(a_elements) == 1:
            data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + a_elements[0].attrib['href']
        elif len(a_elements) == 0:
            pass
        save([], data)

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm" ]

for url in urls:
    scrape_table(url)
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

def scrape_table(url):
    download = urlopen(url)
    raw = download.read()
    
    html = fromstring(raw)
    table = html.cssselect('table')[2]
    
    for tr in table.cssselect('tr')[1:]:
        cell_text = [td.text_content() for td in tr.cssselect('td')]
        data = dict(zip(COLUMN_NAMES, cell_text))
        data['num_workers'] = int(data['num_workers'])
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        data['expiration_date'] = datetime.datetime.strptime(
            data['expiration_date'],
            '%m-%d-%y'
        ).date()
    
        a_elements = tr.cssselect('a')
        if len(a_elements) > 1:
            raise ValueError('Row has multiple a tags.')
        elif len(a_elements) == 1:
            data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + a_elements[0].attrib['href']
        elif len(a_elements) == 0:
            pass
        save([], data)

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm" ]

for url in urls:
    scrape_table(url)
