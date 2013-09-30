import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div.content")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("div.bookInfo a")
        if table_cells: 
            record['Book'] = table_cells[0].text
        table_cells2 = row.cssselect("div.bookInfo span")
        if table_cells2: 
            record['Author'] = table_cells2[1].text
        table_cells3 = row.cssselect("div.highlightedBy")
        if table_cells3: 
            record['Highlighted_by'] = table_cells3[0].text   
            scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Book' : table_cells[0].text,'Author' : table_cells2[1].text,'Passage' : table_cells2[2].text,'Highlighted_by' : table_cells3[0].text})
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("form#seeMoreForm a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


base_url = 'https://kindle.amazon.com/'
starting_url = urlparse.urljoin(base_url, 'search/popular_highlights?keywords=healthcare&start=1')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div.content")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("div.bookInfo a")
        if table_cells: 
            record['Book'] = table_cells[0].text
        table_cells2 = row.cssselect("div.bookInfo span")
        if table_cells2: 
            record['Author'] = table_cells2[1].text
        table_cells3 = row.cssselect("div.highlightedBy")
        if table_cells3: 
            record['Highlighted_by'] = table_cells3[0].text   
            scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Book' : table_cells[0].text,'Author' : table_cells2[1].text,'Passage' : table_cells2[2].text,'Highlighted_by' : table_cells3[0].text})
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("form#seeMoreForm a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


base_url = 'https://kindle.amazon.com/'
starting_url = urlparse.urljoin(base_url, 'search/popular_highlights?keywords=healthcare&start=1')
scrape_and_look_for_next_link(starting_url)
