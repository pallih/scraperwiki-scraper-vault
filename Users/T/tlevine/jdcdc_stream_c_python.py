from scraperwiki.sqlite import save, select
from scraperwiki import pdftoxml
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime
from time import sleep

print dir(datetime)

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

def apples():
    download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
    rawhtml = download.read()
    
    html = fromstring(rawhtml)
    tables = html.cssselect('table')
    table = tables[2]
    
    trs = table.cssselect('tr')
    for tr in trs[1:]:
        tds = tr.cssselect('td')
        cell_values = [td.text_content() for td in tds]
        data = dict(zip(COLUMN_NAMES, cell_values))
        print data
        
        #state
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        
        data['num_workers'] = int(data['num_workers'])
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
    
        links = tr.cssselect('a')
        if len(links) == 1:
            data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + links[0].attrib['href']
        elif len(links) > 1:
            assert False
    
        print data
        save([], data)



apples()

data = select('pdf from swdata')
for row in data:
    pdfurl = row['pdf']
    
    rawpdf = urlopen(pdfurl).read()
    pdfxml = pdftoxml(rawpdf)
    try:
        pdf = fromstring(pdfxml)
    except:
        pass
    else:
        numpages = len(pdf.cssselect('page'))
    
        pdfdata = {'url': pdfurl, 'numpages': numpages}
        save(['url'], pdfdata, 'pdfs')
    sleep(2)