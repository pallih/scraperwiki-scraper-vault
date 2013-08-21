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
    for item in root.cssselect('div[class="page_item"]'):
        name = item.cssselect('a[class="name"]')
        if name: 
            record = { 'link' : name[0].attrib['href'], 'title' : name[0].text }
            # Print out the data we've gathered
            print record
            # Finally, save the record to the datastore - 'link' is our unique key
            scraperwiki.sqlite.save(unique_keys=['link'], data=record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(page):
    print make_page_url(page)
    html = scraperwiki.scrape(make_page_url(page))
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    for next_page in (int(link.text) for link in root.cssselect('*[class="pagination bottom"] a[href]')):
        if next_page > page + 1:
            break
        elif next_page == page + 1: 
            scrape_and_look_for_next_link(next_page)
            break
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://thepagefinder.com/dallas-tx/'
make_page_url = lambda i : urlparse.urljoin(base_url, '?p=' + str(i) + '&s=p')
scrape_and_look_for_next_link(1)
