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

for rest in root.cssselect("div.rating"):

    nm = rest.attrib["onclick"]

    name = nm  

    #rating = rest.cssselect("title")
    #rating = rating.attrib["title"]
    #reviews = rest.cssselect("span")

record={"name": name}
#record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"],record)


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

for rest in root.cssselect("div.rating"):

    nm = rest.attrib["onclick"]

    name = nm  

    #rating = rest.cssselect("title")
    #rating = rating.attrib["title"]
    #reviews = rest.cssselect("span")

record={"name": name}
#record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"],record)


