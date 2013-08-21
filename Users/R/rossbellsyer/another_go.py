import scraperwiki
import csv

# Restaurant Reviews

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

import lxml.html
root = lxml.html.fromstring(html)

for el in root.cssselect("a.bizname_link"):
    print el.text
    
    record = { "name" : el.text}
    scraperwiki.sqlite.save(["name"], record)


for rating in root.cssselect("div.rating"):
    print rating.tail

    

