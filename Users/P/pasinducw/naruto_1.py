import scraperwiki
import lxml.html

html=scraperwiki.scrape("http://www.mangapanda.com/93/naruto.html")
root=lxml.html.fromstring(html)
print root.text_content()
i=0
for a in root.cssselect("table#listing tr a"):
    data={
        "chapterLink": a.attrib['href'],
        "name":a.tail
    }
    #print data
    i=i+1
print "Total Records found: "
print i

import scraperwiki
import lxml.html

html=scraperwiki.scrape("http://www.mangapanda.com/93/naruto.html")
root=lxml.html.fromstring(html)
print root.text_content()
i=0
for a in root.cssselect("table#listing tr a"):
    data={
        "chapterLink": a.attrib['href'],
        "name":a.tail
    }
    #print data
    i=i+1
print "Total Records found: "
print i

