###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.tools.clearsy.com/index.php5?title=Bug_Status'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('td') 
for tr in trs:
    print tr
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.tools.clearsy.com/index.php5?title=Bug_Status'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('td') 
for tr in trs:
    print tr
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    