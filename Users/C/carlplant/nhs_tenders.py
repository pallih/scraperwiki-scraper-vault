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
    rows = root.cssselect("div.srch-results p")  # selects all <a> blocks 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("p.ms-navheader a")
        if table_cells: 
            record['Title'] = table_cells[0].text
            #record['Album'] = table_cells[1].text
            #record['Released'] = table_cells[2].text
            #record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Title"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect(".srch-Page.srch-Page-bg a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'https://www.supply2health.nhs.uk/'
starting_url = urlparse.urljoin(base_url,'results.aspx?k=Status"live"')
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
def scrape_table(root):
    rows = root.cssselect("div.srch-results p")  # selects all <a> blocks 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("p.ms-navheader a")
        if table_cells: 
            record['Title'] = table_cells[0].text
            #record['Album'] = table_cells[1].text
            #record['Released'] = table_cells[2].text
            #record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Title"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect(".srch-Page.srch-Page-bg a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'https://www.supply2health.nhs.uk/'
starting_url = urlparse.urljoin(base_url,'results.aspx?k=Status"live"')
scrape_and_look_for_next_link(starting_url)
