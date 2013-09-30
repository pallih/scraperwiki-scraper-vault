# SCRAPE BY YUSUF NADABO CHANCHANGI 

import scraperwiki
from BeautifulSoup import BeautifulSoup
print "FIRST BEWICKS ARRIVALS AT SLIMBRIDGE"

scraperwiki.metadata.save('data_columns', ['WINTER', 'ARRIVAL DATE', 'FIRST ARRIVALS'])

def scrape_table(soup):
    data_table = soup.find("table", { "class" : "data" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['WINTER'] = table_cells[1].text
            record['ARRIVAL DATE'] = table_cells[2].text
            record['FIRST ARRIVALS'] = table_cells[3].text
            
            print record, '------------'
            # Finally, save the record to the datastore - 'State' is our unique key
            scraperwiki.datastore.save(["WINTER"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)

base_url = 'http://www.guardian.co.uk/news/datablog/2010/oct/19/'
starting_url = base_url + 'arctic-swans-bewick-arrival'
scrape_and_look_for_next_link(starting_url)
# SCRAPE BY YUSUF NADABO CHANCHANGI 

import scraperwiki
from BeautifulSoup import BeautifulSoup
print "FIRST BEWICKS ARRIVALS AT SLIMBRIDGE"

scraperwiki.metadata.save('data_columns', ['WINTER', 'ARRIVAL DATE', 'FIRST ARRIVALS'])

def scrape_table(soup):
    data_table = soup.find("table", { "class" : "data" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['WINTER'] = table_cells[1].text
            record['ARRIVAL DATE'] = table_cells[2].text
            record['FIRST ARRIVALS'] = table_cells[3].text
            
            print record, '------------'
            # Finally, save the record to the datastore - 'State' is our unique key
            scraperwiki.datastore.save(["WINTER"], record)
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = base_url + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)

base_url = 'http://www.guardian.co.uk/news/datablog/2010/oct/19/'
starting_url = base_url + 'arctic-swans-bewick-arrival'
scrape_and_look_for_next_link(starting_url)
