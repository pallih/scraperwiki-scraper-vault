from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring

URL = 'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
muffin = scrape(URL)
print(muffin)

banana = fromstring(muffin)
print(tostring(banana))

tea = banana.cssselect('table')
you = tea[2]

marcus = you.cssselect('tr')
for jay in marcus:
    tractor = jay.cssselect('td,th')
    for apple in tractor:
        print apple.text_content()
        from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring

URL = 'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
muffin = scrape(URL)
print(muffin)

banana = fromstring(muffin)
print(tostring(banana))

tea = banana.cssselect('table')
you = tea[2]

marcus = you.cssselect('tr')
for jay in marcus:
    tractor = jay.cssselect('td,th')
    for apple in tractor:
        print apple.text_content()
        