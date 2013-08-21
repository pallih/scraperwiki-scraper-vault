###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.google.com/finance/historical?q=NYSE:SPY')
print html

soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

scraperwiki.metadata.save('data_columns', ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

def scrape_table(soup):
    data_table = soup.find("table", { "id" : "gf-table historical_price" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Date'] = table_cells[0].text
            record['Open'] = table_cells[1].text
            record['High'] = table_cells[2].text
            record['Low'] = table_cells[3].text
            record['Close'] = table_cells[4].text
            record['Volume'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            scraperwiki.datastore.save(["Date"], record)
            
scrape_table(soup)

