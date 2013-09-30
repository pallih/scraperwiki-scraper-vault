###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.birminghampost.net/news/2012/04/12/birmingham-city-council-elections-candidates-for-2012-65233-30749629/')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
ID_number = 1
for td in tds:
    ID_number = ID_number + 1
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for td in tds:
     record = { "td" : td.text, "tag" : td.tag, "ID" : ID_number } # column name and value
     scraperwiki.sqlite.save(["ID"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.birminghampost.net/news/2012/04/12/birmingham-city-council-elections-candidates-for-2012-65233-30749629/')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
ID_number = 1
for td in tds:
    ID_number = ID_number + 1
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for td in tds:
     record = { "td" : td.text, "tag" : td.tag, "ID" : ID_number } # column name and value
     scraperwiki.sqlite.save(["ID"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

