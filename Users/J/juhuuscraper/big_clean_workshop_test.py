import datetime
from urllib2 import urlopen
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring

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
urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    source = urlopen(url).read()
    html = fromstring(source)
    html.make_links_absolute(url)
    tables = html.cssselect('table')
    table = tables[1]
    
    trs = table.cssselect('tr')
    
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        row_list = [td.text_content() for td in tds]
        row_dict = dict(zip(COLUMN_NAMES, row_list))
        
        row_dict['num_workers'] = int(row_dict['num_workers'])
        state_code = row_dict['location'][:2]
        if state_code in STATES:
            row_dict['state'] = state_code
        else:
            row_dict['state'] = ''
    
        row_dict['expiration_date'] = datetime.datetime.strptime(row_dict['expiration_date'], '%m-%d-%y').date()
        links = tr.cssselect('a')
        if len(links) == 0:
            pass
        elif len(links) == 1:
            link = links[0]
            print tostring(link)
            print link.attrib['href']
            row_dict['pdf_link'] = link.xpath('@href')[0]
        else:
            htnsaoeuhtnsaoeuhtnsaoeu
    
        row_dict['url'] = url
        save([], row_dict, 'agreement')
        print row_dict
import datetime
from urllib2 import urlopen
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring

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
urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    source = urlopen(url).read()
    html = fromstring(source)
    html.make_links_absolute(url)
    tables = html.cssselect('table')
    table = tables[1]
    
    trs = table.cssselect('tr')
    
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        row_list = [td.text_content() for td in tds]
        row_dict = dict(zip(COLUMN_NAMES, row_list))
        
        row_dict['num_workers'] = int(row_dict['num_workers'])
        state_code = row_dict['location'][:2]
        if state_code in STATES:
            row_dict['state'] = state_code
        else:
            row_dict['state'] = ''
    
        row_dict['expiration_date'] = datetime.datetime.strptime(row_dict['expiration_date'], '%m-%d-%y').date()
        links = tr.cssselect('a')
        if len(links) == 0:
            pass
        elif len(links) == 1:
            link = links[0]
            print tostring(link)
            print link.attrib['href']
            row_dict['pdf_link'] = link.xpath('@href')[0]
        else:
            htnsaoeuhtnsaoeuhtnsaoeu
    
        row_dict['url'] = url
        save([], row_dict, 'agreement')
        print row_dict
