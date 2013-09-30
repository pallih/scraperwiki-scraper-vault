

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.citypopulation.de/India-AndhraPradesh.html'
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


import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.citypopulation.de/India-AndhraPradesh.html'
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
