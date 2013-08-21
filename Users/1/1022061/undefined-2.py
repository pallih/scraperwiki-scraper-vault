                                                                     
                                                                     
                                                                     
                                             
import scraperwiki
from BeautifulSoup import BeautifulSoup


   scraperwiki.metadata.save('data_columns', ['DATE', 'NUMBER OF USERS', '% WORLD POPULATION', 'INFORMATION SOURCE'])


def scrape_table(soup):
    data_table = soup.find("table", {"class" : "reference"})
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['DATE'] = table_cells[0].text
            record['NUMBER OF USERS'] = table_cells[1].text
            record['% WORLD POPULATION'] = table_cells[2].text
            record['INFORMATION SOURCE'] = table_cells[3].text
            print record, '------------'
            scraperwiki.datastore.save(["DATE"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url = 'http://www.allaboutmarketresearch.com/internet.htm'
scrape_and_look_for_next_link(starting_url)

