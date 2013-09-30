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

#List of column names
COLNAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    page = urlopen(url)
    html = page.read()
    
    x = fromstring(html)
    tables = x.cssselect('table')
    table = tables[2]
    
    rows = table.cssselect('tr')
    for row in rows[1:]:
        cells = row.cssselect('td,th')
        cell_text = [cell.text_content() for cell in cells]
        data = dict(zip(COLNAMES, cell_text))
    
        data['num_workers'] = int(data['num_workers'])
        state = data['location'][0:2]
        if state in STATES:
            data['state'] = state
        else:
            data['state'] = None
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        links = row.cssselect('a')
        if len(links) == 1:
            data['pdf'] = links[0].attrib['href']
    
        save([], data, 'asdfasdf')from urllib2 import urlopen
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

#List of column names
COLNAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    page = urlopen(url)
    html = page.read()
    
    x = fromstring(html)
    tables = x.cssselect('table')
    table = tables[2]
    
    rows = table.cssselect('tr')
    for row in rows[1:]:
        cells = row.cssselect('td,th')
        cell_text = [cell.text_content() for cell in cells]
        data = dict(zip(COLNAMES, cell_text))
    
        data['num_workers'] = int(data['num_workers'])
        state = data['location'][0:2]
        if state in STATES:
            data['state'] = state
        else:
            data['state'] = None
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        links = row.cssselect('a')
        if len(links) == 1:
            data['pdf'] = links[0].attrib['href']
    
        save([], data, 'asdfasdf')from urllib2 import urlopen
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

#List of column names
COLNAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    page = urlopen(url)
    html = page.read()
    
    x = fromstring(html)
    tables = x.cssselect('table')
    table = tables[2]
    
    rows = table.cssselect('tr')
    for row in rows[1:]:
        cells = row.cssselect('td,th')
        cell_text = [cell.text_content() for cell in cells]
        data = dict(zip(COLNAMES, cell_text))
    
        data['num_workers'] = int(data['num_workers'])
        state = data['location'][0:2]
        if state in STATES:
            data['state'] = state
        else:
            data['state'] = None
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        links = row.cssselect('a')
        if len(links) == 1:
            data['pdf'] = links[0].attrib['href']
    
        save([], data, 'asdfasdf')