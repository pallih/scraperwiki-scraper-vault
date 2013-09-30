import scraperwiki

html = scraperwiki.scrape("http://espn.go.com/college-sports/football/recruiting/school/_/id/2483/oregon")

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    #tds = tr.cssselect("td")
    for item in tr:
        print item.text


import scraperwiki

html = scraperwiki.scrape("http://espn.go.com/college-sports/football/recruiting/school/_/id/2483/oregon")

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    #tds = tr.cssselect("td")
    for item in tr:
        print item.text


