##############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################http://scraperwiki.com/scrapers/new/python?fork=dcrestaurantinspection

import scraperwiki
html = scraperwiki.scrape('http://president.ie/index.php?section=6&engagement=2011&lang=eng')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <strong> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <strong></strong> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------
import BeautifulSoup
import lxml.html

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

#import scraperwiki




root = lxml.html.fromstring(html) # turn our HTML into an lxml object
time_place = 'none'
time = 'none'
place = 'none'

time_places = root.cssselect('strong') # get all the <strong> tags
for time_place in time_places:
    print lxml.html.tostring(time_place) # the full HTML tag
    print time_place.text                # just the text inside the HTML tag

for time_place in time_places:
    
#time, place = time_place.split("(")[1] #.split("<")[0]
#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")
    time, place = time_place.split("/(",1) #[2].split(",")[1].strip().split(" ")
    print time
    print place
# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for time_place in time_places:
#     record = { "td" : td.text } # column name and value
record = { "place" : place, "time" : time } # column name and value.text
scraperwiki.sqlite.save(["place"],["time"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------##############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################http://scraperwiki.com/scrapers/new/python?fork=dcrestaurantinspection

import scraperwiki
html = scraperwiki.scrape('http://president.ie/index.php?section=6&engagement=2011&lang=eng')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <strong> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <strong></strong> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------
import BeautifulSoup
import lxml.html

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

#import scraperwiki




root = lxml.html.fromstring(html) # turn our HTML into an lxml object
time_place = 'none'
time = 'none'
place = 'none'

time_places = root.cssselect('strong') # get all the <strong> tags
for time_place in time_places:
    print lxml.html.tostring(time_place) # the full HTML tag
    print time_place.text                # just the text inside the HTML tag

for time_place in time_places:
    
#time, place = time_place.split("(")[1] #.split("<")[0]
#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")
    time, place = time_place.split("/(",1) #[2].split(",")[1].strip().split(" ")
    print time
    print place
# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for time_place in time_places:
#     record = { "td" : td.text } # column name and value
record = { "place" : place, "time" : time } # column name and value.text
scraperwiki.sqlite.save(["place"],["time"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------##############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################http://scraperwiki.com/scrapers/new/python?fork=dcrestaurantinspection

import scraperwiki
html = scraperwiki.scrape('http://president.ie/index.php?section=6&engagement=2011&lang=eng')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <strong> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <strong></strong> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------
import BeautifulSoup
import lxml.html

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

#import scraperwiki




root = lxml.html.fromstring(html) # turn our HTML into an lxml object
time_place = 'none'
time = 'none'
place = 'none'

time_places = root.cssselect('strong') # get all the <strong> tags
for time_place in time_places:
    print lxml.html.tostring(time_place) # the full HTML tag
    print time_place.text                # just the text inside the HTML tag

for time_place in time_places:
    
#time, place = time_place.split("(")[1] #.split("<")[0]
#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")
    time, place = time_place.split("/(",1) #[2].split(",")[1].strip().split(" ")
    print time
    print place
# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for time_place in time_places:
#     record = { "td" : td.text } # column name and value
record = { "place" : place, "time" : time } # column name and value.text
scraperwiki.sqlite.save(["place"],["time"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------##############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################http://scraperwiki.com/scrapers/new/python?fork=dcrestaurantinspection

import scraperwiki
html = scraperwiki.scrape('http://president.ie/index.php?section=6&engagement=2011&lang=eng')
print "Click on the ...more link to see the whole page"
print html

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <strong> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <strong></strong> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------
import BeautifulSoup
import lxml.html

import httplib2
from glob import glob
from lxml.html import parse
from BeautifulSoup import BeautifulSoup
import re
import sys
import string

#import scraperwiki




root = lxml.html.fromstring(html) # turn our HTML into an lxml object
time_place = 'none'
time = 'none'
place = 'none'

time_places = root.cssselect('strong') # get all the <strong> tags
for time_place in time_places:
    print lxml.html.tostring(time_place) # the full HTML tag
    print time_place.text                # just the text inside the HTML tag

for time_place in time_places:
    
#time, place = time_place.split("(")[1] #.split("<")[0]
#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")
    time, place = time_place.split("/(",1) #[2].split(",")[1].strip().split(" ")
    print time
    print place
# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE THREE LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for time_place in time_places:
#     record = { "td" : td.text } # column name and value
record = { "place" : place, "time" : time } # column name and value.text
scraperwiki.sqlite.save(["place"],["time"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------