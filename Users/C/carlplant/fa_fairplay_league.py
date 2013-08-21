import scraperwiki
import urlparse
import lxml.html


def scrape_table(root):
    rows = root.cssselect("table.fairplay tr")  # selects all <tr> blocks within <table class="fairplay">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            record['Position'] = table_cells[0].text
            record['Games'] = table_cells[2].text
            record['Cautions'] = table_cells[3].text
            record['Dismissals'] = table_cells[4].text
            record['Disc_points'] = table_cells[5].text
            table_cells2 = row.cssselect("a")
            if table_cells2: 
                record['Team'] = table_cells2[0].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Team' is our unique key
            scraperwiki.datastore.save(["Team"], record)
        

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


base_url = 'http://www.thefa.com/football-rules-governance/'
starting_url = urlparse.urljoin(base_url, 'fairplay')
scrape_and_look_for_next_link(starting_url)
