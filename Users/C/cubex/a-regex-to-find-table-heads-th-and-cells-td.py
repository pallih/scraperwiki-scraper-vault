###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
html = scraperwiki.scrape('http://ecoconsulting.co.uk/index.shtml')
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the tags we want.
# BeautifulSoup is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
r1 = r'h.' # regex in quotes after r
tags = soup.findAll('h1')
tags += soup.findAll('h2')
for r1 in tags:
    print r1.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# Check the 'Data' tab to see the saved data. 
# -----------------------------------------------------------------------------

for r1 in tags:
     record = { "r1" : r1.text } # column name and value
     scraperwiki.sqlite.save(["r1"], record) # save the records one by one

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
html = scraperwiki.scrape('http://ecoconsulting.co.uk/index.shtml')
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the tags we want.
# BeautifulSoup is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
r1 = r'h.' # regex in quotes after r
tags = soup.findAll('h1')
tags += soup.findAll('h2')
for r1 in tags:
    print r1.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# Check the 'Data' tab to see the saved data. 
# -----------------------------------------------------------------------------

for r1 in tags:
     record = { "r1" : r1.text } # column name and value
     scraperwiki.sqlite.save(["r1"], record) # save the records one by one

