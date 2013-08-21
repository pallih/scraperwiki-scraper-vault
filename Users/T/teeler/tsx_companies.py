import scraperwiki
import urlparse
import lxml.html
from itertools import izip, islice

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    # All rows but the first (header)
    rows = root.cssselect("table.companyResults tr")[1:-1]  # selects all <tr> blocks within <table class="data">
    i = 0
    # consume a company

    while i < len(rows):
        company_name = rows[i].cssselect("th.symbolGroup a")[0].text
        i += 1
        # consume all tickers
        while i < len(rows) and rows[i].get('class') != "oddRow":
            record = {}
            name = rows[i].cssselect("td")[0].text
            ticker = rows[i].cssselect("td a")[0].text
            record['stock_name'] = name
            record['name'] = company_name
            record['symbol'] = ticker

            print name + ", " + ticker
            i += 1    
            scraperwiki.datastore.save(["symbol"], record) # save the records one by one
                      
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = [t.get('href') for t in root.cssselect("td a") if t.text == 'Next >']

    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0])
        #print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

from string import ascii_uppercase

base_url = 'http://www.tmxmoney.com'

base_path = urlparse.urljoin(base_url, '/HttpController?' +\
           'GetPage=ListedCompanyDirectory&SearchCriteria=Name&' +\
           'SearchKeyword=%s&SearchType=StartWith&Page=1&SearchIsMarket=Yes&Market=T&Language=en')

for c in ascii_uppercase + "0123456789":
    url = base_path % c
    scrape_and_look_for_next_link(url)
