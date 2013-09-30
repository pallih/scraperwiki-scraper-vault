                                                                     
                                                                     
                                                                     
                                             
import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['2010', 'Win7', 'Vista', 'Win2003','WinXP','W2000','Linux','Mac'])


def scrape_table(soup):
    data_table = soup.find("table", {"class" : "reference"})
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['2010'] = table_cells[0].text
            record['Win7'] = table_cells[1].text
            record['Vista'] = table_cells[2].text
            record['Win2003'] = table_cells[3].text
            record['WinXP'] = table_cells[4].text
            record['W2000'] = table_cells[5].text
            record['Linux'] = table_cells[6].text
            record['Mac'] = table_cells[7].text
            print record, '------------'
            scraperwiki.datastore.save(["2010"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://www.w3schools.com/browsers/browsers_os.asp'
scrape_and_look_for_next_link(starting_url)
                                                                     
                                                                     
                                                                     
                                             
import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['2010', 'Win7', 'Vista', 'Win2003','WinXP','W2000','Linux','Mac'])


def scrape_table(soup):
    data_table = soup.find("table", {"class" : "reference"})
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['2010'] = table_cells[0].text
            record['Win7'] = table_cells[1].text
            record['Vista'] = table_cells[2].text
            record['Win2003'] = table_cells[3].text
            record['WinXP'] = table_cells[4].text
            record['W2000'] = table_cells[5].text
            record['Linux'] = table_cells[6].text
            record['Mac'] = table_cells[7].text
            print record, '------------'
            scraperwiki.datastore.save(["2010"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://www.w3schools.com/browsers/browsers_os.asp'
scrape_and_look_for_next_link(starting_url)
