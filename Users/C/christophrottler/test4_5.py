###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.ub.uni-kassel.de/1673.html?&L=2%20and%20char%28124%29%2Buser%2Bchar%28124%29%3D0')


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('h3') # get all the <td> tags
for h3 in tds:
    print lxml.html.tostring(h3) # the full HTML tag
    print h3.text                # just the text inside the HTML tag



for h3 in tds:
     record = { "h3" : h3.text } # column name and value
     scraperwiki.sqlite.save(["h3"], record) # save the records one by one
