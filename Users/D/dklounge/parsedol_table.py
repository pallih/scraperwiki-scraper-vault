import scraperwiki
import datetime

# Scrapes DOL data table set

from urllib2 import urlopen
from lxml.html import fromstring, tostring # because html is not text, we need to convert back to string
from scraperwiki.sqlite import save

# List of column names
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

download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
raw = download.read()
# print download.read()

html = fromstring(raw)
table = html.cssselect('table')[2]   # used to search for a table (or an object)

for tr in table.cssselect('tr')[1:]:  # we don't want the first row of header info
    cell_text = [td.text_content() for td in tr.cssselect('td')]    
    # print COLUMN_NAMES    
    # print cell_text
    data = dict(zip(COLUMN_NAMES, cell_text)) # dictionaries don't keep order, now ready for database
    print data
    data['num_workers'] = int(data['num_workers'])
    if data['location'][:2] in STATES:
        data ['state'] = data['location'][:2]
    a_elements = tr.cssselect('a')

    print datetime.datetime.strptime(
        data['expiration_date'],
        '%m-%d-%y').date()

    if len(a_elements) > 1:
        raise ValueError('Row has multiple a tags.')
    elif len(a_elements) == 1:
        data['pdf']= a_elements[0].attrib['href']
    elif len(a_elements) == 0:
        pass
    
    # print data
    save([], data)

#    for td in tr.cssselect('td'):
# td = tr.cssselect('td')[0] # indicates array element to pull
# print tostring(td)  # prints tag elements
# html.cssselect('table')
# print tostring(html)
# for tr in table.cssselect('tr'):


  