from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring # importing parsing library, like BeautifulSoup

URL = 'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
page = scrape(URL)
# print(page)

content = fromstring(page)
# print(content)

# print(tostring(content))

tbl = content.cssselect('table')
t = tbl[2]

rows = t.cssselect('tr')

row = rows[9]

cells = row.cssselect('td, th')

# cell = cells[4]

# print tostring(cell)
# print cell.text_content()

for cell in cells:
    print cell.text_content()




marcus = you.cssselect('tr')
for jay in marcus:
    tractor = jay.cssselect('td,th')
    for apple in tractor:
        print apple.text_content()
from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring,tostring # importing parsing library, like BeautifulSoup

URL = 'http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
page = scrape(URL)
# print(page)

content = fromstring(page)
# print(content)

# print(tostring(content))

tbl = content.cssselect('table')
t = tbl[2]

rows = t.cssselect('tr')

row = rows[9]

cells = row.cssselect('td, th')

# cell = cells[4]

# print tostring(cell)
# print cell.text_content()

for cell in cells:
    print cell.text_content()




marcus = you.cssselect('tr')
for jay in marcus:
    tractor = jay.cssselect('td,th')
    for apple in tractor:
        print apple.text_content()
