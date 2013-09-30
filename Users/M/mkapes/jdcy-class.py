from scraperwiki import *
from scraperwiki.sqlite import *
from lxml.html import fromstring, tostring


URL='http://www.dol.gov/olms/regs/compliance/cba/index.html'

def filing_data(URL):
    data=scrape(URL)
    data = fromstring(data)
    
    data = data.cssselect('table')
    colnames=[
          'employer','download','location','union',
          'local', 'naics', 'num_workers', 'expiration_date'
    ]
    
    for i in data:
        tablerows= i.cssselect('tr')
        for j in tablerows:
            rowelements=j.cssselect('td')
       
            rowdata=dict(zip( colnames, [k.text_content() for k in rowelements]))
            rowdata['num_workers']= int(rowdata.get('num_workers', 0))
            rowdata['state']= rowdata.get('state', '').strip()[0:2]
            #rowdata['expiration_date']= datetime.datetime.strptime(rowdata.get('expiration_date', '').split(-), "%m, %d, %y")
            
            save([], rowdata)
            
           
orig_data=from_string(scrape(URL))
links=orig_data.from scraperwiki import *
from scraperwiki.sqlite import *
from lxml.html import fromstring, tostring


URL='http://www.dol.gov/olms/regs/compliance/cba/index.html'

def filing_data(URL):
    data=scrape(URL)
    data = fromstring(data)
    
    data = data.cssselect('table')
    colnames=[
          'employer','download','location','union',
          'local', 'naics', 'num_workers', 'expiration_date'
    ]
    
    for i in data:
        tablerows= i.cssselect('tr')
        for j in tablerows:
            rowelements=j.cssselect('td')
       
            rowdata=dict(zip( colnames, [k.text_content() for k in rowelements]))
            rowdata['num_workers']= int(rowdata.get('num_workers', 0))
            rowdata['state']= rowdata.get('state', '').strip()[0:2]
            #rowdata['expiration_date']= datetime.datetime.strptime(rowdata.get('expiration_date', '').split(-), "%m, %d, %y")
            
            save([], rowdata)
            
           
orig_data=from_string(scrape(URL))
links=orig_data.