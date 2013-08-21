from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

#print tostring(html)
#text_content() allows to get plain text inside HTML element
#zip - zips together 2 lists

#List of column names
COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

#list of states
STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
rawtext = page.read()
html = fromstring(rawtext)

#print tostring(html)

tables = html.cssselect('table')
table = tables[2]

for tr in table.cssselect('tr')[1:]:
    cellvalues = [td.text_content() for td in tr.cssselect('td')]
    data = dict(zip(COLUMN_NAMES, cellvalues))
    data['num_workers'] =  int(data['num_workers'])
    data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'],'%m-%d-%y')

    state = data['location'][:2] 
    if state in STATES:
        data['state'] = state
    links = tr.cssselect('a')
    if len(links) == 1:
        data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/'+ links[0].attrib['href']
    print data
    save([], data)