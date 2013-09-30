# bestplaces states and links

print "Running States"

# imports

import csv
import scraperwiki
from BeautifulSoup import BeautifulSoup

#code

html = scraperwiki.scrape("http://www.bestplaces.net/find/default.aspx")

import lxml.html
root = lxml.html.fromstring(html)

for tr in root.cssselect("[valign='top'] p"):
    tag = BeautifulSoup(lxml.html.tostring(tr))
    for tagproperties in tag.findAll('a', {'href': True}):
        BestPlacesStateLink = tagproperties.attrMap['href']
        StateAbr = BestPlacesStateLink.split("=")
        StateName = tagproperties.contents
        
        data = {
        'Link' : BestPlacesStateLink,
        'USPSCode' : StateAbr [1],
        'State' : StateName[0]
        }
        scraperwiki.sqlite.save(unique_keys=['Link'],data=data)





    # bestplaces states and links

print "Running States"

# imports

import csv
import scraperwiki
from BeautifulSoup import BeautifulSoup

#code

html = scraperwiki.scrape("http://www.bestplaces.net/find/default.aspx")

import lxml.html
root = lxml.html.fromstring(html)

for tr in root.cssselect("[valign='top'] p"):
    tag = BeautifulSoup(lxml.html.tostring(tr))
    for tagproperties in tag.findAll('a', {'href': True}):
        BestPlacesStateLink = tagproperties.attrMap['href']
        StateAbr = BestPlacesStateLink.split("=")
        StateName = tagproperties.contents
        
        data = {
        'Link' : BestPlacesStateLink,
        'USPSCode' : StateAbr [1],
        'State' : StateName[0]
        }
        scraperwiki.sqlite.save(unique_keys=['Link'],data=data)





    