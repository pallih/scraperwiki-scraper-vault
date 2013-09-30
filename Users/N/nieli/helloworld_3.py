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
    rows = root.cssselect("""a."name bold notranslate" """)  # selects all <tr> blocks within <table class="data">
    print root
    print 1
    print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row
        print table_cells
        if table_cells:
            record['ProjectURL'] = table_cells[0].attrib.get('href')
            record['ProjectName'] = table_cells[0].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ProjectURL"], record)
        
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
##base_url = 'http://www.madingley.org/uploaded/'
base_url = 'http://www.indiegogo.com'
middle_url = '/projects?filter_category=Small+Business&filter_country=CTRY_US&filter_location=on&pbigg_id=1&pg_num='
ending_url = '&utf8=%E2%9C%93'

max_page = 1

for page_number in range(max_page):
    url = base_url + middle_url + str(page_number+1) + ending_url
    #print url
    #html = scraperwiki.scrape(url)
    root = lxml.html.parse(url).getroot()
    #print html
    #root = lxml.html.fromstring(html)
    scrape_table(root)
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
    rows = root.cssselect("""a."name bold notranslate" """)  # selects all <tr> blocks within <table class="data">
    print root
    print 1
    print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row
        print table_cells
        if table_cells:
            record['ProjectURL'] = table_cells[0].attrib.get('href')
            record['ProjectName'] = table_cells[0].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ProjectURL"], record)
        
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
##base_url = 'http://www.madingley.org/uploaded/'
base_url = 'http://www.indiegogo.com'
middle_url = '/projects?filter_category=Small+Business&filter_country=CTRY_US&filter_location=on&pbigg_id=1&pg_num='
ending_url = '&utf8=%E2%9C%93'

max_page = 1

for page_number in range(max_page):
    url = base_url + middle_url + str(page_number+1) + ending_url
    #print url
    #html = scraperwiki.scrape(url)
    root = lxml.html.parse(url).getroot()
    #print html
    #root = lxml.html.fromstring(html)
    scrape_table(root)
