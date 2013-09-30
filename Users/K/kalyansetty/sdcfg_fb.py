# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup
import urlparse
import lxml.html
scraperwiki.sqlite.get_var('data_columns')

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    data_table = root.find("table", { "class" : "body sortable" })
    rows = data_table.findAll("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Rank'] = table_cells[0].text
            record['Countries'] = table_cells[1].text
            record['Amount'] = table_cells[2].text
            #record['Rating'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Countries"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.nationmaster.com/graph/mil_aid_to_afg_gro_dis_as_a_per_of_oda-afghanistan-gross-disbursements-percent-oda'
scrape_and_look_for_next_link(base_url)# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup
import urlparse
import lxml.html
scraperwiki.sqlite.get_var('data_columns')

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    data_table = root.find("table", { "class" : "body sortable" })
    rows = data_table.findAll("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Rank'] = table_cells[0].text
            record['Countries'] = table_cells[1].text
            record['Amount'] = table_cells[2].text
            #record['Rating'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Countries"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.nationmaster.com/graph/mil_aid_to_afg_gro_dis_as_a_per_of_oda-afghanistan-gross-disbursements-percent-oda'
scrape_and_look_for_next_link(base_url)