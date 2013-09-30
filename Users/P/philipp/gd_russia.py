import scraperwiki
import lxml.html   
rows = []

print "hello"
html = scraperwiki.scrape("http://www.duma.gov.ru/about/personnel/property/deputies/?letter=Б%91&print=yes")

root = lxml.html.fromstring(html)
print len(root)
print str(root[0])
base = root.cssselect('div [id="left-col"]')
#base = base.cssselect('div [id="left-col"]')[0]
#base = base.cssselect('div [class="table-data td-filter"]')[0]
#base = base.cssselect('table [id="financy-table"]')

#base = base.cssselect('tr')
#d = base[3].cssselect('td')
#i = 0
#for tr in base:
#    x = tr.cssselect('td')
#    print x[0].text    



#table id="financy-table"
#head = base.cssselect('h2')

print len(root), ': ', len(base)
#print base

import scraperwiki
import lxml.html   
rows = []

print "hello"
html = scraperwiki.scrape("http://www.duma.gov.ru/about/personnel/property/deputies/?letter=Б%91&print=yes")

root = lxml.html.fromstring(html)
print len(root)
print str(root[0])
base = root.cssselect('div [id="left-col"]')
#base = base.cssselect('div [id="left-col"]')[0]
#base = base.cssselect('div [class="table-data td-filter"]')[0]
#base = base.cssselect('table [id="financy-table"]')

#base = base.cssselect('tr')
#d = base[3].cssselect('td')
#i = 0
#for tr in base:
#    x = tr.cssselect('td')
#    print x[0].text    



#table id="financy-table"
#head = base.cssselect('h2')

print len(root), ': ', len(base)
#print base

