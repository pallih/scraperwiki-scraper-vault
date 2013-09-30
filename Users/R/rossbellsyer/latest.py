import scraperwiki
import csv

# Restaurant Reviews

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

import lxml.html
root = lxml.html.fromstring(html)

#busname
for name in root.cssselect("a.bizname_link"):
#    print name.text
    
    name=name.text
    #record = {"name" : name}
    #scraperwiki.sqlite.save(["name"], name)


#get rating
for rating in root.cssselect("div.rating span"):

    rating = rating.attrib["title"]
   

#get numreviews
for numreviews in root.cssselect("div.rating span"):

    numreviews = numreviews.tail


    record={"name": name, "rating": rating, "numreview": numreviews}

    scraperwiki.sqlite.save(["numreview"],record)

import scraperwiki
import csv

# Restaurant Reviews

html = scraperwiki.scrape("http://www.menus.co.nz/restaurants/?f=New+Zealand")

import lxml.html
root = lxml.html.fromstring(html)

#busname
for name in root.cssselect("a.bizname_link"):
#    print name.text
    
    name=name.text
    #record = {"name" : name}
    #scraperwiki.sqlite.save(["name"], name)


#get rating
for rating in root.cssselect("div.rating span"):

    rating = rating.attrib["title"]
   

#get numreviews
for numreviews in root.cssselect("div.rating span"):

    numreviews = numreviews.tail


    record={"name": name, "rating": rating, "numreview": numreviews}

    scraperwiki.sqlite.save(["numreview"],record)

