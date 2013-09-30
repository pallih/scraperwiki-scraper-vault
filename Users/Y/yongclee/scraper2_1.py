import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

#List of column names
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

#print page.read()

rawtext = page.read()

html = fromstring(rawtext)

#print html
#print tostring(html)

tables = html.cssselect('table')
table = tables[1]

print table.cssselect('tr') #cssselect = lxml?
td = tr.cssselect('td')[3]
print td.text_content()

for tr in table.cssselect('tr')[1:]:
    #print td.text_content()
    cellvalues = [td.text_content() for td in tr.cssselect('td')]
    data = dict(zip(COLUMN_NAMES, cellvalues)) #zip joins column_names and cellvalues
    data['num_workers'] = int(data['num_workers'])
    data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'],'%m-%d-%y').date() #strptime() takes raw expiration_date, matches to format you specify
    #print data['location'][0:2]
    state = data['location'][0:2]
    if state in STATES:
        data['state'] = state
    links = tr.cssselect('a')
    if len(links) ==1:
        data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + links[0].attrib['href']
    save ([], data)    

import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

#List of column names
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

#print page.read()

rawtext = page.read()

html = fromstring(rawtext)

#print html
#print tostring(html)

tables = html.cssselect('table')
table = tables[1]

print table.cssselect('tr') #cssselect = lxml?
td = tr.cssselect('td')[3]
print td.text_content()

for tr in table.cssselect('tr')[1:]:
    #print td.text_content()
    cellvalues = [td.text_content() for td in tr.cssselect('td')]
    data = dict(zip(COLUMN_NAMES, cellvalues)) #zip joins column_names and cellvalues
    data['num_workers'] = int(data['num_workers'])
    data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'],'%m-%d-%y').date() #strptime() takes raw expiration_date, matches to format you specify
    #print data['location'][0:2]
    state = data['location'][0:2]
    if state in STATES:
        data['state'] = state
    links = tr.cssselect('a')
    if len(links) ==1:
        data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + links[0].attrib['href']
    save ([], data)    

