#Name: Arun Kumar Bussa ,student number:0925005,email: Arun.Bussa@wlv.ac.uk.The  scrapper tabulates the rankings of #the countries in accordance with the number of females suffering from breast cancer. 
import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['Rank', 'Countries', 'Amount'])


def scrape_table(soup):
    data_table = soup.find("table", { "class" : "body sortable" })
    rows = data_table.findAll("tr")
    for row in rows:
        
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Rank'] = table_cells[0].text
            record['Countries'] = table_cells[1].text
            record['Amount'] = table_cells[2].text
            
            
            print record, '------------'
            
            scraperwiki.datastore.save(["Countries"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url ='http://www.nationmaster.com/graph/hea_bre_can_inc-health-breast-cancer-incidence'
scrape_and_look_for_next_link(starting_url)

#Name: Arun Kumar Bussa ,student number:0925005,email: Arun.Bussa@wlv.ac.uk.The  scrapper tabulates the rankings of #the countries in accordance with the number of females suffering from breast cancer. 
import scraperwiki
from BeautifulSoup import BeautifulSoup


scraperwiki.metadata.save('data_columns', ['Rank', 'Countries', 'Amount'])


def scrape_table(soup):
    data_table = soup.find("table", { "class" : "body sortable" })
    rows = data_table.findAll("tr")
    for row in rows:
        
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Rank'] = table_cells[0].text
            record['Countries'] = table_cells[1].text
            record['Amount'] = table_cells[2].text
            
            
            print record, '------------'
            
            scraperwiki.datastore.save(["Countries"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url ='http://www.nationmaster.com/graph/hea_bre_can_inc-health-breast-cancer-incidence'
scrape_and_look_for_next_link(starting_url)

