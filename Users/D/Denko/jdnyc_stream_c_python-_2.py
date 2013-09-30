from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring
import datetime

COLNAMES=[
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

def saveFilingTable(url):
    muffin = scrape(url)
    
    banana = fromstring(muffin)
    
    tea = banana.cssselect('table')
    you=tea[2]
    
    marcus = you.cssselect('tr')
    for jay in marcus[1:]:
        tractor = jay.cssselect('td,th')
        aidan = [apple.text_content() for apple in tractor]
        data  = dict(zip(COLNAMES,aidan))
        print(data)
        data['state']=data['location'].strip()[0:2]
        data['num_workers']=int(data['num_workers'])
        if data['state'] not in [ 'Na',
      'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
      'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
      'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
      'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
      'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            data['state']='unknown'
        v = map(int,data['expiration_date'].split('-'))
        data['expiration_date'] = datetime.date(v[2]+2000,v[0],v[1])
        #data['expiration_date'] = datetime.datetime.strptime(
        #    data['expiration_date'],
        #    '%m-%d-%y'
        #).date()
        #print(data)
        save([],data)

saveFilingTable(URL)from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring
import datetime

COLNAMES=[
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'

def saveFilingTable(url):
    muffin = scrape(url)
    
    banana = fromstring(muffin)
    
    tea = banana.cssselect('table')
    you=tea[2]
    
    marcus = you.cssselect('tr')
    for jay in marcus[1:]:
        tractor = jay.cssselect('td,th')
        aidan = [apple.text_content() for apple in tractor]
        data  = dict(zip(COLNAMES,aidan))
        print(data)
        data['state']=data['location'].strip()[0:2]
        data['num_workers']=int(data['num_workers'])
        if data['state'] not in [ 'Na',
      'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
      'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
      'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
      'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
      'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            data['state']='unknown'
        v = map(int,data['expiration_date'].split('-'))
        data['expiration_date'] = datetime.date(v[2]+2000,v[0],v[1])
        #data['expiration_date'] = datetime.datetime.strptime(
        #    data['expiration_date'],
        #    '%m-%d-%y'
        #).date()
        #print(data)
        save([],data)

saveFilingTable(URL)