import scraperwiki
import urlparse 
import lxml.html 

def scrape_table(root):
    rows = root.cssselect("table.data tr")
    for rows in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record["title"] = table_cells[0].text 
            record["citations"] = table_cells[1].text 
            record["year"] = table_cells[3].text 
            print record 
            scraperwiki.datastore.save(["title"], record)



def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape("http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works")
    print html 
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = lxml.html.cssselect("a.next")
    print next_link
    if next_linl:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

for i in range(0,20):
    starting_url = urlparse.urljoin(base_url, "&cstart=0 + 20")

base_url = "http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works"
scrape_and_look_for_next_link(starting_url)
