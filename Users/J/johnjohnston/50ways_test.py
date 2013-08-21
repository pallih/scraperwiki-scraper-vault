import scraperwiki

# Blank Python
           
import lxml.html
html = scraperwiki.scrape("http://50ways.wikispaces.com/Tools+A+to+Z")
root = lxml.html.fromstring(html)
for el in root.cssselect("li.includePageListPage a"):           
    print lxml.html.tostring(el)
    data = {'link' : lxml.html.tostring(el)
        }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
print data