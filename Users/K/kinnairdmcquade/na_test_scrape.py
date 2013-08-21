###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import mechanize 
import urlparse
import lxml.html

nameetingsurl = "http://na.org/?ID=phoneline"

br = mechanize.Browser()
response = br.open(nameetingsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="div.body")
print br.form

br["st_usa_search"] = "01/01/2004"
br["$state_province"] = ["[USA] Alabama"]


# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Description'] = table_cells[0].text
            record['Phone Number and Website'] = table_cells[1].text
            record['Country Name'] = table_cells[2].text
            record['State'] = table_cells[4].text
            record['Area Code'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Area Names"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://na.org/?ID=phoneline'
starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(starting_url)
