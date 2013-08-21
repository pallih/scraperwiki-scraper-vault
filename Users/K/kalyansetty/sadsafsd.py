import scraperwiki
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    scraperwiki.metadata.save('data_columns', ['When','Movie title','Language','Uploader'])
    tbl = root.find("table", {"border":"0"})
    rows = tbl.findAll("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if len(table_cells) == 4: 
            record['When'] = table_cells[0].text
            record['Movie title'] = table_cells[1].text
            record['Language'] = table_cells[2].text
            record['Uploader'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Movie title"], record)
        
#--------------------------------------------------------------------------
base_url = 'http://www.divxsubtitles.net/'
getdata=scraperwiki.scrape(base_url)
root = BeautifulSoup(getdata)
scrape_table(root)
