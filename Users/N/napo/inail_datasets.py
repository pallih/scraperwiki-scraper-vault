import scraperwiki
import lxml.html
html = scraperwiki.scrape('http://dati.inail.it/opendata/index.jsp?action=4')

root = lxml.html.fromstring(html) 
tables = root.cssselect('table th') 
for table in tables:
    print lxml.html.tostring(table)
    for elements in table:
        for e in elements:
            print lxml.html.tostring(e)
            #print e[0]
print root
import scraperwiki
import lxml.html
html = scraperwiki.scrape('http://dati.inail.it/opendata/index.jsp?action=4')

root = lxml.html.fromstring(html) 
tables = root.cssselect('table th') 
for table in tables:
    print lxml.html.tostring(table)
    for elements in table:
        for e in elements:
            print lxml.html.tostring(e)
            #print e[0]
print root
