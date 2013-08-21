###############################################################################
# Current Blood Stocks Scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime

# retrieve a page
starting_url = 'http://www.blood.co.uk/StockGraph/stocklevelstandard.aspx'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)


stocks_table = soup.find('table', {'id': 'GridView_StockLevel'} ) 
rows = stocks_table.findAll('tr')
records = {'date_scraped': str(datetime.now())}
for row in rows[1:-1]: #clip first and last - header/total
    tds = row.findAll('td')
    records.update({ tds[0].text : tds[1].text.replace(',', '') }) #remove ,
    
scraperwiki.datastore.save(["date_scraped"], data=records )

