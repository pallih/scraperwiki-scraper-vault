###############################################################################
# START! HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.condensed tbody tr")
    for row in rows:
        record = {}

        ths = row.cssselect("th")
        if ths:
            record['Name'] = row.cssselect("th a")[0].text

        table_cells = row.cssselect("td")
        if table_cells:
            record['Political Party'] = table_cells[0].text
            record['District'] = table_cells[1].text
            scraperwiki.datastore.save(["Name"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.link-next")
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.praha3.cz/volene-organy/zastupitelstvo/seznam-zastupitelu/'
starting_url = urlparse.urljoin(base_url, 'index.html')
scrape_and_look_for_next_link(starting_url)
