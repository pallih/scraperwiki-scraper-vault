###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
html = scraperwiki.scrape('http://curtis.library.northwestern.edu/curtis/toc.cgi')
#print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
vols = soup.findAll('h3') # get all the <td> tags
for vol in vols:
#    print td # the full HTML tag
    match = re.search(r'Vol.*', vol.text)
    if match:
        print vol.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for vol in vols:
    match = re.search(r'Vol.*', vol.text)
    if match:
        record = { "vol" : vol.text } # column name and value
        scraperwiki.datastore.save(["vol"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
html = scraperwiki.scrape('http://curtis.library.northwestern.edu/curtis/toc.cgi')
#print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
vols = soup.findAll('h3') # get all the <td> tags
for vol in vols:
#    print td # the full HTML tag
    match = re.search(r'Vol.*', vol.text)
    if match:
        print vol.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

for vol in vols:
    match = re.search(r'Vol.*', vol.text)
    if match:
        record = { "vol" : vol.text } # column name and value
        scraperwiki.datastore.save(["vol"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

