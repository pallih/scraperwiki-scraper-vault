###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.studentenwerk-kassel.de/faq.html')


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('h3') # get all the <td> tags
for h3 in tds:
    print lxml.html.tostring(h3) # the full HTML tag
    print h3.text                # just the text inside the HTML tag



for h3 in tds:
     record = { "h3" : h3.text } # column name and value
     scraperwiki.sqlite.save(["h3"], record) # save the records one by one



import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('p') # get all the <td> tags
for p in tds:
    print lxml.html.tostring(p) # the full HTML tag
    print p.text                # just the text inside the HTML tag



for p in tds:
     record = { "p" : p.text } # column name and value
     scraperwiki.sqlite.save(["p"], record) # save the records one by one