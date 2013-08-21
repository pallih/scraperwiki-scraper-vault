import scraperwiki
from BeautifulSoup import BeautifulSoup

url = "http://info.csa.com/political/classcodes.shtml"
html = scraperwiki.scrape(url)


# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find('table',width="84%")
    #print data_table
    trows = data_table.findAll("tr")
    for trow in trows:
        #record = {}
        #print trow
        # Set up our data record - we'll need it later
        rows = trow.findAll("td")
        for row in rows:
            #print row
            record = {}
            table_cells = row.findAll("span")
            if table_cells:
                record['Code'] = table_cells[0].text
    #            print sp
    #    rows2 = row.findAll("td")
    #    for column in columns:
    #    rows = data_table.findAll("span", { "class" : "style42"} )
    #    for row2 in rows2:        
    #        print row2
    #    if table_cells:
    #         record['Code'] = table_cells[0].text   
    #        record['Code1'] = table_cells[0].text
    #        record['Code2'] = table_cells[1].text
                print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
                scraperwiki.datastore.save(["Code"], record)



# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code'])
soup = BeautifulSoup(html)
scrape_table(soup)
