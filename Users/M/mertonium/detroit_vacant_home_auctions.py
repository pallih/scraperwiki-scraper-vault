###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
single_family_url = 'http://www.ci.detroit.mi.us/'
html = scraperwiki.scrape(single_family_url)
print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#container = soup.find("div", {"id": "dnn_ctr1826_Display_HtmlHolder"})
#print container
#options = soup.find("select", { "id" : "ctl00_ContentPlaceHolder1_ddlCrimeType" }).findAll("option")


#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
#    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
single_family_url = 'http://www.ci.detroit.mi.us/'
html = scraperwiki.scrape(single_family_url)
print html
#soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
#container = soup.find("div", {"id": "dnn_ctr1826_Display_HtmlHolder"})
#print container
#options = soup.find("select", { "id" : "ctl00_ContentPlaceHolder1_ddlCrimeType" }).findAll("option")


#tds = soup.findAll('td') 
#for td in tds:
#    print td
#    record = { "td" : td.text }
#    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    