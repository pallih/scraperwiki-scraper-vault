###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.fec.gov/finance/disclosure/ftpsum.shtml'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('tr') 
tds = soup.findAll('td')
hrefs = soup.findAll('a')
for tr in trs:
    print tr
    record = { "tr" : tr.text }
for a in hrefs:
    print a
    record1 = { "a" : a.txt }
for td in tds:
    print td
    record2 = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["tr"], record) 
    scraperwiki.datastore.save(["a"], record1)
    scraperwiki.datastore.save(["td"], record2)###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.fec.gov/finance/disclosure/ftpsum.shtml'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('tr') 
tds = soup.findAll('td')
hrefs = soup.findAll('a')
for tr in trs:
    print tr
    record = { "tr" : tr.text }
for a in hrefs:
    print a
    record1 = { "a" : a.txt }
for td in tds:
    print td
    record2 = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["tr"], record) 
    scraperwiki.datastore.save(["a"], record1)
    scraperwiki.datastore.save(["td"], record2)