import scraperwiki
from BeautifulSoup import BeautifulSoup
html = scraperwiki.scrape('https://www.rec-registry.gov.au/publicSummaryHoldingsReport.shtml?access=public')
print html

soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Category'] = table_cells[0].text
            record['RECs'] = table_cells[1].text
            #record['text2'] = table_cells[3].text
            print record
            scraperwiki.mysql.save(["Category"], record)
            
scrape_table(soup)
