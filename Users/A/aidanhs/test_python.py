###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://scraperwiki.com/hello_world.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td')
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://scraperwiki.com/hello_world.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td')
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)
    