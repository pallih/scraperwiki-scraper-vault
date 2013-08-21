import scraperwiki
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    scraperwiki.metadata.save('data_columns', ['API','Category','Updated','Description'])
    tbl = root.find("table" , {"class":"listTable mB15"})

    
    rows = tbl.findAll("tr")
    
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if len(table_cells) == 4: 
            
            record['API'] = table_cells[0].text
            record['Category'] = table_cells[1].text
            record['Updated'] = table_cells[2].text
            record['Description'] = table_cells[3].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["API"], record)
        
#--------------------------------------------------------------------------
base_url = 'http://www.programmableweb.com/apis/directory/1?sort=date'
getdata=scraperwiki.scrape(base_url)
root = BeautifulSoup(getdata)
scrape_table(root)