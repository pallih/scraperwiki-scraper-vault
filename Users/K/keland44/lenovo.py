# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://outlet.lenovo.com/laptops.html?limit=all")
print html

import lxml.html
root = lxml.html.fromstring(html)
for li in root.cssselect('li'):
    print lxml.html.tostring(li)

for li in root.cssselect('li'):
    data = {'table_cell': li.text} # save data in dictionary
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data) 
# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://outlet.lenovo.com/laptops.html?limit=all")
print html

import lxml.html
root = lxml.html.fromstring(html)
for li in root.cssselect('li'):
    print lxml.html.tostring(li)

for li in root.cssselect('li'):
    data = {'table_cell': li.text} # save data in dictionary
    # Choose unique keyname
    scraperwiki.datastore.save(unique_keys=['table_cell'], data=data) 
