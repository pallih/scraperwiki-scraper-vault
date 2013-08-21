import scraperwiki

# Blank Python

## Uses scraperwiki to scrape fortune 500 companies names and city location in Washington State
## Applies a geocoder module to find physical location.

import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://money.cnn.com/magazines/fortune/fortune500/2012/states/WA.html")
root = lxml.html.fromstring(html)
for tbody in root.cssselect("div[id='cnnmagFeatData'] tbody"):
    #data =[]
    for tr in tbody.cssselect("tr"):     
        tds = tr.cssselect("td")
        data= {
            "Company Name" : tds[1].text_content(),
            "Headquarters City" : tr[3].text_content(),
            "Forbes Company Rank" : tr[2].text_content(),
            "Company Revenue" : tr[4].text_content()
            }
        scraperwiki.sqlite.save(unique_keys=["Company Name","Headquarters City","Forbes Company Rank","Company Revenue"], data=data)

# print data
