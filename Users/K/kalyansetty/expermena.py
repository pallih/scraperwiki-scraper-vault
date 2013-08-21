import scraperwiki
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    scraperwiki.metadata.save('data_columns', ['Posted','Job Title','Company','Job Location'])
    tbl = root.find("table", {"class": "jobListingsTable"})
    rows = tbl.findAll("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if len(table_cells) == 4: 
            record['Posted'] = table_cells[0].text
            record['Job Title'] = table_cells[1].text
            record['Company'] = table_cells[2].text
            record['Job Location'] = table_cells[3].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Company"], record)
        
#--------------------------------------------------------------------------
base_url = 'http://www.payscale.com/research/UK/Job=Data_Analyst/Job-Listings'
getdata=scraperwiki.scrape(base_url)
root = BeautifulSoup(getdata)
scrape_table(root)
