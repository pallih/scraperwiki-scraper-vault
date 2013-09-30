###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html


scraperwiki.sqlite.get_var('data_columns',['Acquisition date', 'Company', 'Business', 'Value (USD)','Derived products'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "wikitable sortable" })
    rows = data_table.findAll("tr")
    #rows = root.cssselect("table.wikitable_sortable tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Acquisition date'] = table_cells[0].text
            record['Company'] = table_cells[1].text
            record['Business'] = table_cells[2].text
            record['Value (USD)'] = table_cells[3].text
            record['Derived products'] = table_cells[4].text

            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Company"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_webpage = 'http://en.wikipedia.org/wiki/List_of_acquisitions_by_Yahoo!'
html = scraperwiki.scrape(base_webpage)
soup = BeautifulSoup(html)
scrape_table(soup)###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html


scraperwiki.sqlite.get_var('data_columns',['Acquisition date', 'Company', 'Business', 'Value (USD)','Derived products'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "wikitable sortable" })
    rows = data_table.findAll("tr")
    #rows = root.cssselect("table.wikitable_sortable tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Acquisition date'] = table_cells[0].text
            record['Company'] = table_cells[1].text
            record['Business'] = table_cells[2].text
            record['Value (USD)'] = table_cells[3].text
            record['Derived products'] = table_cells[4].text

            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Company"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_webpage = 'http://en.wikipedia.org/wiki/List_of_acquisitions_by_Yahoo!'
html = scraperwiki.scrape(base_webpage)
soup = BeautifulSoup(html)
scrape_table(soup)