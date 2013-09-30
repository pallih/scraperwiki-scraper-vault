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

for rest in root.cssselect("div.listing"):

    nm = rest.cssselect("a.bizname_link")[0]

    name = nm.text   

    el = rest.cssselect("div.rating span")[0]
    rating = el.attrib["title"]
    reviews = el.tail

record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"],record)

#scraperwiki.sqlite.execute("insert into swdata values (?, ?, ?)", [name, rating, reviews])
#scraperwiki.sqlite.commit()
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

for rest in root.cssselect("div.listing"):

    nm = rest.cssselect("a.bizname_link")[0]

    name = nm.text   

    el = rest.cssselect("div.rating span")[0]
    rating = el.attrib["title"]
    reviews = el.tail

record={"name": name, "rating" : rating, "reviews": reviews}

scraperwiki.sqlite.save(["name"],record)

#scraperwiki.sqlite.execute("insert into swdata values (?, ?, ?)", [name, rating, reviews])
#scraperwiki.sqlite.commit()
