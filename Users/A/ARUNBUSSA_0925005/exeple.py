###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['#','Species', 'Name','BL','W W','W','Family','Latin name'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['#'] = table_cells[0].text
            record['Species'] = table_cells[1].text
            record['Name'] = table_cells[2].text
            record['BL'] = table_cells[3].text
            record ['W W'] = table_cells[4].text
            record['W'] = table_cells[5].text
            record['Family'] = table_cells[6].text
            record['Latin name'] = table_cells[7].text
            # Print out the data we've gathered
            print record, '------------'
            scraperwiki.datastore.save(["Latin name"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

starting_url = 'http://www.birds-of-north-america.net/list-of-north-american-birds.html'
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['#','Species', 'Name','BL','W W','W','Family','Latin name'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['#'] = table_cells[0].text
            record['Species'] = table_cells[1].text
            record['Name'] = table_cells[2].text
            record['BL'] = table_cells[3].text
            record ['W W'] = table_cells[4].text
            record['W'] = table_cells[5].text
            record['Family'] = table_cells[6].text
            record['Latin name'] = table_cells[7].text
            # Print out the data we've gathered
            print record, '------------'
            scraperwiki.datastore.save(["Latin name"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

starting_url = 'http://www.birds-of-north-america.net/list-of-north-american-birds.html'
scrape_and_look_for_next_link(starting_url)
