###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.thecompleteuniversityguide.co.uk/league-tables/rankings')
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
trs = root.cssselect('tr') # get all the <tr> tags
for tr in trs:
    print lxml.html.tostring(tr) # the full HTML tag
    print tr.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for tr in trs:
     record = { "tr" : tr.text } # column name and value
     scraperwiki.sqlite.save(["2012"], record) # save the records one by one

    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.thecompleteuniversityguide.co.uk/league-tables/rankings')
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
trs = root.cssselect('tr') # get all the <tr> tags
for tr in trs:
    print lxml.html.tostring(tr) # the full HTML tag
    print tr.text                # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for tr in trs:
     record = { "tr" : tr.text } # column name and value
     scraperwiki.sqlite.save(["2012"], record) # save the records one by one

    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

