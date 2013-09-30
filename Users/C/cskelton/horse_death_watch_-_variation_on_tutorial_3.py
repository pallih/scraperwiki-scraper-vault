###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    html = scraperwiki.scrape(starting_url)
    print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table class="data">
    rownumber = 0
    for row in rows:
        rownumber = rownumber + 1
        if rownumber > 40:
            break
        print rownumber
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        print row.text
        if table_cells: 
            table_cellsurls = table_cells[0].cssselect("a")
            record['Horse'] = table_cells[0].text_content()
            record['Date'] = table_cells[1].text_content()
            record['Course'] = table_cells[2].text_content()
            record['Cause of Death'] = table_cells[3].text_content()
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = 'http://horsedeathwatch.com/'
scrape_table(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    html = scraperwiki.scrape(starting_url)
    print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table class="data">
    rownumber = 0
    for row in rows:
        rownumber = rownumber + 1
        if rownumber > 40:
            break
        print rownumber
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        print row.text
        if table_cells: 
            table_cellsurls = table_cells[0].cssselect("a")
            record['Horse'] = table_cells[0].text_content()
            record['Date'] = table_cells[1].text_content()
            record['Course'] = table_cells[2].text_content()
            record['Cause of Death'] = table_cells[3].text_content()
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = 'http://horsedeathwatch.com/'
scrape_table(starting_url)
