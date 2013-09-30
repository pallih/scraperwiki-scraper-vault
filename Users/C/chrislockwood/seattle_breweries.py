import scraperwiki
# Brewery Scraper
# Blank Python

import scraperwiki

import lxml.html

html = scraperwiki.scrape ("http://www.washingtonbeer.com/breweries/seattle-king-co/")
print html

root = lxml.html.fromstring (html)

for p in root.cssselect("div.entry p"):
   
    

    strong = p.cssselect("strong")
    adresslist =  lxml.html.tostring(p).split("<br>")

    print lxml.html.tostring(p)


    data = {
        'brewname' : strong[0].text_content(),
        'address' : adresslist[1]
        }

    print data
    scraperwiki.sqlite.save(['brewname'], data=data)
    

import scraperwiki
# Brewery Scraper
# Blank Python

import scraperwiki

import lxml.html

html = scraperwiki.scrape ("http://www.washingtonbeer.com/breweries/seattle-king-co/")
print html

root = lxml.html.fromstring (html)

for p in root.cssselect("div.entry p"):
   
    

    strong = p.cssselect("strong")
    adresslist =  lxml.html.tostring(p).split("<br>")

    print lxml.html.tostring(p)


    data = {
        'brewname' : strong[0].text_content(),
        'address' : adresslist[1]
        }

    print data
    scraperwiki.sqlite.save(['brewname'], data=data)
    

