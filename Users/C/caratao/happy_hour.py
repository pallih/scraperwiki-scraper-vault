import scraperwiki

# Blank Python

import lxml.html

html = scraperwiki.scrape("http://www.seattlemag.com/article/best-happy-hours-restaurants")
print html

root = lxml.html.fromstring(html)

for p in root.cssselect("div.content p"):

    ps = p.cssselect("span")
    if len(ps)>2:
        resname = ps[2].cssselect("span").text
#    loc =
#    time = 
        print ps, resname

    