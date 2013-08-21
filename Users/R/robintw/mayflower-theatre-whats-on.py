###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.mayflower.org.uk/whatson.asp')
print html



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

print soup.prettify()

titles = soup.findAll(attrs={'class':"woEventName2"})
dates = soup.findAll(attrs={'class': "woEventDates"})
links = soup.findAll(attrs={'class': "woTitle"})


for i in range(len(titles)):
    event = {}
    print titles[i].text
    print dates[i].text
    print links[i]['href']
    
    event['Title'] = titles[i].text
    event['Date'] = dates[i].text
    event['URL'] = "http://www.mayflower.org.uk/" + links[i]['href']
    
    scraperwiki.sqlite.save(["Title"], event) # save the records one by one
