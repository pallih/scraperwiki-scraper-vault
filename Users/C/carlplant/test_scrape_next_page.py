import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div.da-perf-entity-teaser")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("div.ratings span")
        if table_cells: 
            record['Performance'] = table_cells[0].text
        table_cells1 = row.cssselect("div.ratings span")
        if table_cells1:
            record['Patient Satisfaction'] = table_cells1[1].text
            #print record, '------------'
            #rows2 = root.cssselect("div.left h2")  
            #for row2 in rows2:
            table_cells2 = row.cssselect("div.left a")
            if table_cells2:
                record['Trust'] = table_cells2[0].text[0]
                scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Trust' : table_cells2[0].text, 'Patient Satisfaction' : table_cells1[1].text, 'Performance' : table_cells[0].text})
        

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


base_url = 'https://www.nhslocal.nhs.uk/'
starting_url = urlparse.urljoin(base_url, 'perf/search?entype=acute-trust&distance[search_distance]=100&distance[search_units]=mile&distance[postal_code]=cv5%207hd#comp=')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("div.da-perf-entity-teaser")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("div.ratings span")
        if table_cells: 
            record['Performance'] = table_cells[0].text
        table_cells1 = row.cssselect("div.ratings span")
        if table_cells1:
            record['Patient Satisfaction'] = table_cells1[1].text
            #print record, '------------'
            #rows2 = root.cssselect("div.left h2")  
            #for row2 in rows2:
            table_cells2 = row.cssselect("div.left a")
            if table_cells2:
                record['Trust'] = table_cells2[0].text[0]
                scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Trust' : table_cells2[0].text, 'Patient Satisfaction' : table_cells1[1].text, 'Performance' : table_cells[0].text})
        

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


base_url = 'https://www.nhslocal.nhs.uk/'
starting_url = urlparse.urljoin(base_url, 'perf/search?entype=acute-trust&distance[search_distance]=100&distance[search_units]=mile&distance[postal_code]=cv5%207hd#comp=')
scrape_and_look_for_next_link(starting_url)
