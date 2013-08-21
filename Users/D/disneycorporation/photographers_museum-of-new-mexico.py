# Museum of New Mexico Photographers

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.museumofnewmexico.org/mfa/ideaphotographic/artists.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('tr') 
for tr in tds:
    print tr
    record = { "tr" : tr.text }
    # save records to the datastore
    scraperwiki.datastore.save(["tr"], record) 
    