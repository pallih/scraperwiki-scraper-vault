###############################################################################
# Community interest company scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time

# retrieve a page
starting_url = 'http://www.bis.gov.uk/cicregulator/cic-register'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll('tr') 
for tr in trs:
    if tr.find(colspan="3"):
        continue
    elif tr.contents[1].contents[0]==" Name of company ":
        continue
    else:
        name = tr.contents[1].contents
        if len(name)>1:
            name = tr.contents[1].contents[1]
        else:
            name = tr.contents[1].contents[0]
        name = name.replace('&amp;','&')
        conum = tr.contents[3].contents[0]
        try:
            location = tr.contents[5].contents[0]
        except IndexError:
            location = "NO LOCATION"
        location = location.replace('&amp;','&')
        try:
            incorp = tr.contents[7].contents[0]
        except IndexError:
            incorp = ""
        print name, conum, location, incorp
        record = { "name" : name , "conum" : conum , "location" : location , "incorp" : incorp  }
        # save records to the datastore
        scraperwiki.sqlite.save(["conum"], record) 
    