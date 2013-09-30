#Scrape of NHS Choice to look at numbers of
#people recommending GP practices
#and whether the practice has extended appointment times

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("ul.results li ul")  # selects  <ul> blocks within <"ul.results">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("li h3 a")
        if table_cells: 
            record['Name'] = table_cells[0].text
            #print record, '------------'
        table_cells2 = row.cssselect("li.address")
        if table_cells2: 
            record['Address'] = table_cells2[0].text 
        table_cells3 = row.cssselect("li a")
        if table_cells3: 
            record['Score'] = table_cells3[0].attrib['href']
            print record, '------------'
            scraperwiki.sqlite.save(unique_keys=[], data={'Name' : table_cells[0].text,'link' : table_cells3[0].attrib['href'], 'Address' : table_cells2[0].text})
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.next a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.nhs.uk/ServiceDirectories/Pages/'
starting_url = urlparse.urljoin(base_url, 'ServiceResults.aspx?Postcode=CV5++6HG&Coords=2787%2c4318&ServiceType=WalkInCentre&JScript=1&PageCount=11&PageNumber=1')
scrape_and_look_for_next_link(starting_url)
#Scrape of NHS Choice to look at numbers of
#people recommending GP practices
#and whether the practice has extended appointment times

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("ul.results li ul")  # selects  <ul> blocks within <"ul.results">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("li h3 a")
        if table_cells: 
            record['Name'] = table_cells[0].text
            #print record, '------------'
        table_cells2 = row.cssselect("li.address")
        if table_cells2: 
            record['Address'] = table_cells2[0].text 
        table_cells3 = row.cssselect("li a")
        if table_cells3: 
            record['Score'] = table_cells3[0].attrib['href']
            print record, '------------'
            scraperwiki.sqlite.save(unique_keys=[], data={'Name' : table_cells[0].text,'link' : table_cells3[0].attrib['href'], 'Address' : table_cells2[0].text})
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.next a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.nhs.uk/ServiceDirectories/Pages/'
starting_url = urlparse.urljoin(base_url, 'ServiceResults.aspx?Postcode=CV5++6HG&Coords=2787%2c4318&ServiceType=WalkInCentre&JScript=1&PageCount=11&PageNumber=1')
scrape_and_look_for_next_link(starting_url)
