
from urllib2 import urlopen

from lxml.html import fromstring, tostring



print 'Hello world'



page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
rawtext = page.read()
html = fromstring(rawtext)



tds = html.cssselect('td')
#print tostring(tds[44])

tables = html.cssselect('table')

table = tables[2]
#print tostring('tables')


tr = table.cssselect ('tr')[8]
for td in tr.cssselect('td'):

#td = tr.csselect('td')[3]
     print td.text_conect()

#for table in tables:
#    print tostring(table)


from urllib2 import urlopen

from lxml.html import fromstring, tostring



print 'Hello world'



page = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
rawtext = page.read()
html = fromstring(rawtext)



tds = html.cssselect('td')
#print tostring(tds[44])

tables = html.cssselect('table')

table = tables[2]
#print tostring('tables')


tr = table.cssselect ('tr')[8]
for td in tr.cssselect('td'):

#td = tr.csselect('td')[3]
     print td.text_conect()

#for table in tables:
#    print tostring(table)

