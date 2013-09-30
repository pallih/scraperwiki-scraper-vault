import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://www.un.org/en/members/") ##load site
root = lxml.html.fromstring(html)
for el in root.cssselect("li .countryname a"): ##load css tag to parse
    coun = el.text
    print el
    print el.text

for eD in root.cssselect("li .joindate"):
    jdat = eD.text
    print eD
    print eD.text

    if coun is not None:
        if jdat is not None:
            data = {
                'Country' : coun,
                'Date' : jdat,
            }

    print data
    scraperwiki.sqlite.save(unique_keys=['Country','Date'], data=data)

import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://www.un.org/en/members/") ##load site
root = lxml.html.fromstring(html)
for el in root.cssselect("li .countryname a"): ##load css tag to parse
    coun = el.text
    print el
    print el.text

for eD in root.cssselect("li .joindate"):
    jdat = eD.text
    print eD
    print eD.text

    if coun is not None:
        if jdat is not None:
            data = {
                'Country' : coun,
                'Date' : jdat,
            }

    print data
    scraperwiki.sqlite.save(unique_keys=['Country','Date'], data=data)

