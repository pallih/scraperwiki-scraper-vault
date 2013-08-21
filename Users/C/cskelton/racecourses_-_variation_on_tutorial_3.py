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
    rows = root.cssselect("table")[2]  # selects all <tr> blocks within <table class="data">
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
            mapurls = table_cells[2].cssselect("a")
            record['Racecourse'] = table_cells[0].text_content()
            record['Address'] = table_cells[1].text_content()
            record['MapURL'] = mapurls[0].attrib.get('href')
            record['RaceCourseURL'] = table_cellsurls[0].attrib.get('href')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Racecourse"], record)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = 'http://www.ukjockey.com/maps.html'
scrape_table(starting_url)
