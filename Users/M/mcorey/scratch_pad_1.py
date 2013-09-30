from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring, cssselect
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local','naics','num_workers','expiration_date'
]

total_workers = 0

def run_page(url):
    global total_workers
    download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
    html_raw = download.read()
    html_parsed = fromstring(html_raw)
    
    tables = html_parsed.cssselect('table')
        
    for tr in tables[2].cssselect('tr')[1:]:
        cell_text =  [td.text_content() for td in tr.cssselect('td')]
        data = dict(zip(COLUMN_NAMES, cell_text))
        data['num_workers'] = int(data['num_workers'])
        total_workers += data['num_workers']
    
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        if len(tr.cssselect('a')) == 1:
            data['pdf_link'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + tr.cssselect('a')[0].attrib['href']
    
        print data
        #save([], data)

urls = [
    'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
]

#for url in urls:
#    run_page(url)
    
#print 'Total workers: %s' % total_workers

from scraperwiki import pdftoxml
pdf_url = urlopen('http://www.dol.gov/olms/regs/compliance/cba/private/2431_pri.pdf').read()
print pdftoxml(pdf_url)

from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring, cssselect
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local','naics','num_workers','expiration_date'
]

total_workers = 0

def run_page(url):
    global total_workers
    download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
    html_raw = download.read()
    html_parsed = fromstring(html_raw)
    
    tables = html_parsed.cssselect('table')
        
    for tr in tables[2].cssselect('tr')[1:]:
        cell_text =  [td.text_content() for td in tr.cssselect('td')]
        data = dict(zip(COLUMN_NAMES, cell_text))
        data['num_workers'] = int(data['num_workers'])
        total_workers += data['num_workers']
    
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        if len(tr.cssselect('a')) == 1:
            data['pdf_link'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + tr.cssselect('a')[0].attrib['href']
    
        print data
        #save([], data)

urls = [
    'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
]

#for url in urls:
#    run_page(url)
    
#print 'Total workers: %s' % total_workers

from scraperwiki import pdftoxml
pdf_url = urlopen('http://www.dol.gov/olms/regs/compliance/cba/private/2431_pri.pdf').read()
print pdftoxml(pdf_url)

