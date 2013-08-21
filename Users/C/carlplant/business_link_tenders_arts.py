import scraperwiki
import urlparse
import lxml.html
import datetime
now = datetime.datetime.now()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.separate tbody tr")  # selects all <tr> blocks within <table class="data">
    #print rows
    for row in rows:
        record = {}
        table_cells = row.cssselect("td a.notice-title")
        if table_cells: 
            Tender = table_cells[0].text
            Link = table_cells[0].attrib['href']
        table_cells2 = row.cssselect("td p.italicise")
        if table_cells2: 
            Details = table_cells2[0].text
        table_cells3 = row.cssselect("td.tablecell-width-2")
        if table_cells3:
            location = table_cells3[0].text_content()
        table_cells4 = row.cssselect("td.tablecell-width-3")
        if table_cells4:
            date = table_cells4[0].text_content()
        table_cells5 = row.cssselect("td.corners-right.tablecell-width-4")
        if table_cells5:
            Value = table_cells5[0].text_content()
            scraperwiki.sqlite.save(unique_keys=[], data={'Scrape_date' : now, 'Tender' :Tender,'Details':Details,'Location':location,'Date':date,'Value':Value,'Link':Link})
        

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.pager-next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


base_url = 'http://www.contractsfinder.businesslink.gov.uk/'
starting_url = urlparse.urljoin(base_url, 'Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=dcb2c8ca-b6ec-495f-8e7a-c14b75b4739f&osc=6e9de4fe-4b98-43ba-88fc-7b1a65e5682a&rb=1')
scrape_and_look_for_next_link(starting_url)
