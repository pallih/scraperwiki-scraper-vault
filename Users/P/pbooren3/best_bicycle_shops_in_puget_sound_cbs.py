import scraperwiki

# Peter Booren
# 
# GEOG 495
# Best Bicycle Shops in Puget Sound Scraper (Source: CBS)


import lxml.html
html = scraperwiki.scrape ("http://seattle.cbslocal.com/2012/03/23/best-bicycle-shops-in-puget-sound/")

print html

root = lxml.html.fromstring (html)

for a in root.cssselect("div.entry a"):
    
    strong = a.cssselect("strong")
    adresslist = lxml.html.tostring(p[1]).split("<br>")

    print lxml.html.tostring(a)

