import scraperwiki
import lxml.html
import csv
import re

# Restaurant Reviews

record={}

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

root = lxml.html.fromstring(html)
#root = lxml.html.etree.HTML(html)

#busname

for nm in root.cssselect("a.bizname_link"):

    name = nm.text    

el = root.cssselect("div.rating span")[0]
rating = el.attrib["title"]
reviews = el.tail

record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"], record)
import scraperwiki
import lxml.html
import csv
import re

# Restaurant Reviews

record={}

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

root = lxml.html.fromstring(html)
#root = lxml.html.etree.HTML(html)

#busname

for nm in root.cssselect("a.bizname_link"):

    name = nm.text    

el = root.cssselect("div.rating span")[0]
rating = el.attrib["title"]
reviews = el.tail

record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"], record)
