import scraperwiki

# Blank Python

print "Mercer - Unit prices - Personal Superannuation Division"

html = scraperwiki.scrape('https://secure.superfacts.com/public/mst/upc.tpz?hc=mtpsd&TP=PL_Unit_prices_3')

#print html

import lxml.html
root = lxml.html.fromstring(html)

for td in root.cssselect("div[align='left'] td"):
    tds = tr.cssselect("td")
#    if len(tds)==12:
    data = {
        'Investment' : tds[0].text_content(),
        'Entry' : int(tds[4].text_content(),
        'Exit' : int(tds[4].text_content(),
        'Current Entry' : int(tds[4].text_content(),
        'Current Exit' : int(tds[4].text_content())
        }
        print data

