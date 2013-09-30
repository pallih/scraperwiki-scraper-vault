###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text_content()                # just the text inside the HTML tag

for td in tds:
     record = { "td" : td.text_content() } # column name and value
     scraperwiki.sqlite.save(["td"], record) # save the records one by one
    

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text_content()                # just the text inside the HTML tag

for td in tds:
     record = { "td" : td.text_content() } # column name and value
     scraperwiki.sqlite.save(["td"], record) # save the records one by one
    

