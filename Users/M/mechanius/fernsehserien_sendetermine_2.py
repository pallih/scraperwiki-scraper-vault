import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.sendetermine tbody")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        sendetermin = {}
        table_cells = row.cssselect("tr td")
        if table_cells:
            sendetermin['wochentag'] = table_cells[0].text_content()
            sendetermin['datum'] = table_cells[1].text_content()
            sendetermin['start'] = table_cells[2].text_content().encode('ascii','replace').split('?')[0]
            sendetermin['ende'] = table_cells[2].text_content().encode('ascii','replace').split('?')[1]
            sendetermin['sender'] = table_cells[3].text_content()
            sendetermin['episode'] = table_cells[4].text_content()+table_cells[5].text_content()
            sendetermin['titel'] = table_cells[6].text_content()
            sendetermin['episodeguideurl'] = row.attrib['data-href']
            # Print out the data we've gathered
            print sendetermin , '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(['datum','sender','start'], sendetermin)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = next_link = root.xpath('//a[starts-with(text(), "weiter")]')
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.fernsehserien.de/the-big-bang-theory/sendetermine/'
starting_url = urlparse.urljoin(base_url, 'prosieben/-23')
scrape_and_look_for_next_link(starting_url)
