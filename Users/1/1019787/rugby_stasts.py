import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.metadata.save('data_columns',['Rank','Countries', 'Amount ','Date'])

def scrape_table(soup):
    data_table = soup.find("table",{"class":"body sortable"})
    rows = data_table.findAll("tr", recursive=False)
    for row in rows:
        
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Rank'] = table_cells[0].text
            record['Countries'] = table_cells[1].text
            record['Amount'] = table_cells[2].text
            record['Date'] = table_cells[3].text
            
            print record, '------------'
            scraperwiki.datastore.save(["Rank"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url =  'http://www.nationmaster.com/graph/eco_gdp_percap-economy-gdp-per-capita'
scrape_and_look_for_next_link(starting_url)