from scraperwiki.sqlite import save
from urllib2 import urlopen 
from lxml.html import fromstring, tostring




page=urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

rawtext = page.read()
html = fromstring(rawtext)

#print tostring(html)



tables=html.cssselect('table')
table=tables[2]

for tr in table.cssselect('tr')[8]
    print tostring(tr)










from scraperwiki.sqlite import save
from urllib2 import urlopen 
from lxml.html import fromstring, tostring




page=urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')

rawtext = page.read()
html = fromstring(rawtext)

#print tostring(html)



tables=html.cssselect('table')
table=tables[2]

for tr in table.cssselect('tr')[8]
    print tostring(tr)










