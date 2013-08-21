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
    rows = root.cssselect("h3 a")  # selects all <h3> blocks 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Headline'] = row.text_content()
        record['URL'] = baseurl+row.attrib.get('href')
        print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
baseurl = 'http://www.irishtimes.com'
starting_url = baseurl+'/ireland/'
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
    rows = root.cssselect("h3 a")  # selects all <h3> blocks 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Headline'] = row.text_content()
        record['URL'] = baseurl+row.attrib.get('href')
        print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
baseurl = 'http://www.irishtimes.com'
starting_url = baseurl+'/ireland/'
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
    rows = root.cssselect("h3 a")  # selects all <h3> blocks 
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        record['Headline'] = row.text_content()
        record['URL'] = baseurl+row.attrib.get('href')
        print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
baseurl = 'http://www.irishtimes.com'
starting_url = baseurl+'/ireland/'
scrape_and_look_for_next_link(starting_url)
