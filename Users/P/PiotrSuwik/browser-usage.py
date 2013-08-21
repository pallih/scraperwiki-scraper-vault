###############################################################################
# Piotr Suwik Scraper - Web browsers usage statistics month by month
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

#Define columns
scraperwiki.metadata.save('data_columns', ['Browser', 'Year', 'Month', 'Usage %'])

# retrieve a page
starting_url = 'http://www.w3schools.com/browsers/browsers_stats.asp'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    #scraperwiki.datastore.save(["td"], record) 
    
