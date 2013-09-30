import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.metadata.save('data_columns',['rank','country',' airport','city','IATA/ICAO code','total passengers','change'])

def scrape_table(soup):
    data_table = soup.find("table",{"class":"wikitable sortable"})
    rows1 = data_table.findAll("tbody")

    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['rank'] = table_cells[0].text
            record['country'] = table_cells[1].text
            record['airport'] = table_cells[2].text
            record['city'] = table_cells[3].text
            record['IATA/ICAO code'] = table_cells[4].text
            record['total passengers'] = table_cells[5].text
            record['change'] = table_cells[6].text
            
            
            print record,'------------'
            scraperwiki.datastore.save(["rank"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url =  "http://en.wikipedia.org/wiki/List_of_the_busiest_airports_in_Asia"
scrape_and_look_for_next_link(starting_url)import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.metadata.save('data_columns',['rank','country',' airport','city','IATA/ICAO code','total passengers','change'])

def scrape_table(soup):
    data_table = soup.find("table",{"class":"wikitable sortable"})
    rows1 = data_table.findAll("tbody")

    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['rank'] = table_cells[0].text
            record['country'] = table_cells[1].text
            record['airport'] = table_cells[2].text
            record['city'] = table_cells[3].text
            record['IATA/ICAO code'] = table_cells[4].text
            record['total passengers'] = table_cells[5].text
            record['change'] = table_cells[6].text
            
            
            print record,'------------'
            scraperwiki.datastore.save(["rank"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    


starting_url =  "http://en.wikipedia.org/wiki/List_of_the_busiest_airports_in_Asia"
scrape_and_look_for_next_link(starting_url)