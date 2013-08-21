import scraperwiki
from BeautifulSoup import BeautifulSoup
print "STARTED RUNNING"


scraperwiki.metadata.save('data_columns', ['WINTER', 'ARRIVAL DATE', 'FIRST ARRIVALS'])


def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            
            record['WINTER'] = table_cells[0].text
          
            record['FIRST ARRIVALS'] = table_cells[2].text
           
            
            print record, '            '
            scraperwiki.datastore.save(["FIRST ARRIVALS"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)


starting_url =  'http://www.guardian.co.uk/news/datablog/2010/oct/19/arctic-swans-bewick-arrival'
scrape_and_look_for_next_link(starting_url)
