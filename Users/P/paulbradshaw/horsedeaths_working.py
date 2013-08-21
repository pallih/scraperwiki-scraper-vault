###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Horse'] = table_cells[0].text_content()
            #... label 'album': the text in the second [1] table_cells item...    
            table_cellsurls = table_cells[0].cssselect("a")
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Horse'] = table_cells[0].text_content()
            #... label 'album': the text in the second [1] table_cells item...    
            table_cellsurls = table_cells[0].cssselect("a")
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
