###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://www.odesk.com/login.php'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://www.odesk.com/login.php'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
    