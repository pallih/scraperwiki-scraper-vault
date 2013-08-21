###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.python.org/community/jobs/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
divs = soup.findAll('div', {'class':'section'})
for div in divs:
    h2 = div.find('h2').text
    print h2, 
    record = { 
              "id" : div['id'], 
              "name": h2,
              "info": div.text
             }
    # save records to the datastore
    scraperwiki.datastore.save(["id", "name", "info"], record) 
    