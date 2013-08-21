import scraperwiki
from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring,tostring
# Blank Python
#print('Hello World')
#download = urlopen("http://newshackdaysf.tumblr.com")
#print download

download = urlopen("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
print download
#print download.read()
raw = download.read()
html = fromstring(raw)
table = html.cssselect('table')[2]
for tr in table.cssselect('tr'):
    for td in tr.cssselect('td'):
        print [td.text_content() for td in tr.cssselect('td')]

#table = html.cssselect('table')[2]
#for tr in table.cssselect('tr'):
#    for td in tr.cssselect('td'):
#        print td.text_content()

#for tr in table.cssselect('tr'):
#    print tostring(table.cssselect('tr')
#print table.cssselect('tr')
#print tostring(table)


#html = fromstring(raw)
#print tostring(html)


