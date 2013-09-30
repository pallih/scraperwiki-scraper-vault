###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Name', 'Address', 'TK', 'Area', 'Tel'])

html = scraperwiki.scrape('http://www.fsth.gr/efhmereu_farmak.asp?ef_date=07/11/2010')
soup = BeautifulSoup(html)

    data_table = soup.find("table", { "class" : "fsth_tex" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Address'] = table_cells[1].text
            record['TK'] = table_cells[2].text
            record['Area'] = table_cells[3].text
            record['Tel'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Name"], record)
        
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Name', 'Address', 'TK', 'Area', 'Tel'])

html = scraperwiki.scrape('http://www.fsth.gr/efhmereu_farmak.asp?ef_date=07/11/2010')
soup = BeautifulSoup(html)

    data_table = soup.find("table", { "class" : "fsth_tex" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Address'] = table_cells[1].text
            record['TK'] = table_cells[2].text
            record['Area'] = table_cells[3].text
            record['Tel'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Name"], record)
        
