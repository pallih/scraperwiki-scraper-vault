###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.met.rdg.ac.uk/~brugge/web_snowdepth.html')

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
pre = soup.findAll('pre') # get all the <td> tags
data = pre[0].text

lines = data.split("\n")
print len(lines)

for line in lines:
    cols = line.split()
    if len(cols) != 7:
        continue
    reading = {}
    reading['Year'] = cols[0]
    reading['Month'] = cols[1]
    reading['Day'] = cols[2]
    reading['Hour'] = cols[3]
    reading['SiteNum'] = cols[4]
    reading['Depth'] = cols[5]
    reading['Location'] = cols[6]

    scraperwiki.datastore.save(['Year', 'Month', 'Day', 'Hour', 'Location'], reading) # save the records one by one

print "Done"
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.met.rdg.ac.uk/~brugge/web_snowdepth.html')

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
pre = soup.findAll('pre') # get all the <td> tags
data = pre[0].text

lines = data.split("\n")
print len(lines)

for line in lines:
    cols = line.split()
    if len(cols) != 7:
        continue
    reading = {}
    reading['Year'] = cols[0]
    reading['Month'] = cols[1]
    reading['Day'] = cols[2]
    reading['Hour'] = cols[3]
    reading['SiteNum'] = cols[4]
    reading['Depth'] = cols[5]
    reading['Location'] = cols[6]

    scraperwiki.datastore.save(['Year', 'Month', 'Day', 'Hour', 'Location'], reading) # save the records one by one

print "Done"
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

