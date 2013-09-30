###############################################################################
# Basic scraper
###############################################################################

import scraperwiki, datetime
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ratesetter.com/lender_market_view.aspx?term=1'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('span', {"class": "bignumber"}) 
monthly = tds[0].text.strip(' %')


starting_url = 'http://www.ratesetter.com/lender_market_view.aspx?term=36'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('span', {"class": "bignumber"}) 
threeyear= tds[0].text.strip(' %')





record = { "month" : monthly , "threeyear" : threeyear, "date" : datetime.datetime.now()}
# save records to the datastore
scraperwiki.sqlite.save(["date"], record) 
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki, datetime
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ratesetter.com/lender_market_view.aspx?term=1'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('span', {"class": "bignumber"}) 
monthly = tds[0].text.strip(' %')


starting_url = 'http://www.ratesetter.com/lender_market_view.aspx?term=36'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('span', {"class": "bignumber"}) 
threeyear= tds[0].text.strip(' %')





record = { "month" : monthly , "threeyear" : threeyear, "date" : datetime.datetime.now()}
# save records to the datastore
scraperwiki.sqlite.save(["date"], record) 
    