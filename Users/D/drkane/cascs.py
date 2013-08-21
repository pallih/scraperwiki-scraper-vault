###############################################################################
# CASC scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time

# retrieve a page
starting_url = 'http://www.hmrc.gov.uk/casc/clubs.htm'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
paras = soup.findAll(id='centre_col')
for a in paras:
    anchors = a.findAll('a')
    for b in anchors:
        try:
            length = len(b.text)
        except ValueError:
            length = 0
        if length==1:
            page_url = 'http://www.hmrc.gov.uk/casc/' + b['href']
            page_html = scraperwiki.scrape(page_url)
            #print url
            page_soup = BeautifulSoup(page_html)
            trs = page_soup.findAll('tr') 
            for tr in trs:
                tds = tr.findAll('td')
                if len(tds)==0:
                    continue
                else:
                    try:
                        name = tds[0].contents[0]
                    except IndexError:
                        name = ""
                    try:
                        address = tds[1].contents[0]
                    except IndexError:
                        address = ""
                    try:
                        postcode = tds[2].contents[0]
                    except IndexError:
                        postcode = ""
                    print name, address, postcode
                    record = { "name" : name , "address" : address , "postcode" : postcode }
                    scraperwiki.sqlite.save(["name"], record) 

