from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring
import datetime
import re


apple = scrape("http://www.dol.gov/olms/regs/compliance/cba/")
print(apple)












urls = ['http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm']

for eve in urls:
    download=scrape(eve)
    
    page=fromstring(download)
    print page
    print download
    
    tables=page.cssselect('table')
    print(tables)
    for table in tables:
        print(tostring(table))
    
    table=tables[2]
    trs=table.cssselect('tr')
    
    tr=trs[4]
    tds=tr.cssselect('td,th')
    
    #data={"firstname":"Albert","lastname":"Einstein"}
    #save([],data)
    
    COLNAMES = [
        'employer','download','location','union',
        'local', 'naics', 'num_workers', 'expiration_date'
    ]
    
    print tostring(trs[0])
    print tostring(trs[1])
    
    del trs[0]
    header_row=trs.pop(0)
    trs = trs[1:]
    
    for tr in trs:
        tds=tr.cssselect('td,th')
        bart = [td.text_content() for td in tds]
        data = dict(zip(COLNAMES,bart))
        data['num_workers'] = int(data['num_workers'])
        ed = data['expiration_date'].split('-')
        data['expiration_date'] = datetime.date(int(ed[2])+2000, int(ed[0]), int(ed[1]))
        data['state_code'] = data['location'].strip()[0:2]
        if data['state_code'] not in ['Na', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            data['state_code'] = "unknown"
        data['url']=eve
        print data
        print bart
        save([],data)
    

"""
Put this in the slides and outline

['employer','download',...]
['city market','pdf',...]
{"employer":"city market","download":"pdf"

"""

#50 minutes at tostring(trs[4])
"""Take a break after
for tr in trs:
    for td in tds:
        print tostring(td)
        print(td.text_content())


Demonstrate the copy stuff at the beginning.
* Remind me to click save

Name functions more weirdly, like x and y.

Do only 10 trs to make things cleaner.

After getting the parse of one page, we do the SQL
"""from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring
import datetime
import re


apple = scrape("http://www.dol.gov/olms/regs/compliance/cba/")
print(apple)












urls = ['http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm']

for eve in urls:
    download=scrape(eve)
    
    page=fromstring(download)
    print page
    print download
    
    tables=page.cssselect('table')
    print(tables)
    for table in tables:
        print(tostring(table))
    
    table=tables[2]
    trs=table.cssselect('tr')
    
    tr=trs[4]
    tds=tr.cssselect('td,th')
    
    #data={"firstname":"Albert","lastname":"Einstein"}
    #save([],data)
    
    COLNAMES = [
        'employer','download','location','union',
        'local', 'naics', 'num_workers', 'expiration_date'
    ]
    
    print tostring(trs[0])
    print tostring(trs[1])
    
    del trs[0]
    header_row=trs.pop(0)
    trs = trs[1:]
    
    for tr in trs:
        tds=tr.cssselect('td,th')
        bart = [td.text_content() for td in tds]
        data = dict(zip(COLNAMES,bart))
        data['num_workers'] = int(data['num_workers'])
        ed = data['expiration_date'].split('-')
        data['expiration_date'] = datetime.date(int(ed[2])+2000, int(ed[0]), int(ed[1]))
        data['state_code'] = data['location'].strip()[0:2]
        if data['state_code'] not in ['Na', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']:
            data['state_code'] = "unknown"
        data['url']=eve
        print data
        print bart
        save([],data)
    

"""
Put this in the slides and outline

['employer','download',...]
['city market','pdf',...]
{"employer":"city market","download":"pdf"

"""

#50 minutes at tostring(trs[4])
"""Take a break after
for tr in trs:
    for td in tds:
        print tostring(td)
        print(td.text_content())


Demonstrate the copy stuff at the beginning.
* Remind me to click save

Name functions more weirdly, like x and y.

Do only 10 trs to make things cleaner.

After getting the parse of one page, we do the SQL
"""