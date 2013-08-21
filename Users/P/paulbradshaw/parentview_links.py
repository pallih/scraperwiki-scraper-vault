import scraperwiki
import urlparse
import lxml.html


def scrape_table(root):
    lis = root.cssselect("ul.linkList li")  # selects all <li> within <ul class="linkList">
    for li in lis:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = li.cssselect("a")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['URL'] = table_cells[0].attrib.get('href')
            print record, '------------'
            # Ssave the record to the datastore - 'URL' is our unique key
            scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.pager-next a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://parentview.ofsted.gov.uk'
starting_url = urlparse.urljoin(base_url, '/parent-view-results/search?page=0')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html


def scrape_table(root):
    lis = root.cssselect("ul.linkList li")  # selects all <li> within <ul class="linkList">
    for li in lis:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = li.cssselect("a")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['URL'] = table_cells[0].attrib.get('href')
            print record, '------------'
            # Ssave the record to the datastore - 'URL' is our unique key
            scraperwiki.datastore.save(["URL"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.pager-next a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://parentview.ofsted.gov.uk'
starting_url = urlparse.urljoin(base_url, '/parent-view-results/search?page=0')
scrape_and_look_for_next_link(starting_url)
