from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring

COLNAMES=[
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
muffin = scrape(URL)

banana = fromstring(muffin)

tea = banana.cssselect('table')
you=tea[2]

marcus = you.cssselect('tr')
for jay in marcus[0:7]:
    tractor = jay.cssselect('td,th')
    aidan = [apple.text_content() for apple in tractor]
    data  = dict(zip(COLNAMES,aidan))
    save([],data)