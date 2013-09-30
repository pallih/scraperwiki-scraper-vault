###############################################################################
# Basic scraper
###############################################################################

import scraperwiki, re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.trafficengland.com/trafficalerts.aspx'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# Get the links
links = soup.findAll('a', href=re.compile('map.aspx\?isTrafficAlert')) 
for link in links:
    print link
    heading = link.text
    parent = link.parent.parent.parent
    detail = parent.text.replace(link.text, "")

    print heading
    print detail
    record = { "alert" : heading + "; " + detail }
    scraperwiki.datastore.save(["alert"], record)



# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki, re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.trafficengland.com/trafficalerts.aspx'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# Get the links
links = soup.findAll('a', href=re.compile('map.aspx\?isTrafficAlert')) 
for link in links:
    print link
    heading = link.text
    parent = link.parent.parent.parent
    detail = parent.text.replace(link.text, "")

    print heading
    print detail
    record = { "alert" : heading + "; " + detail }
    scraperwiki.datastore.save(["alert"], record)



# use BeautifulSoup to get all <td> tags
#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    