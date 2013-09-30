###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.csa.com/factsheets/supplements/saclass.php')


# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table",width="84%")
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            if (len (table_cells) == 3):
                record['Code'] = table_cells[1].text
                record['Title'] = table_cells[2].text
            else :
                record['Code'] = table_cells[0].text
                record['Title'] = table_cells[1].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Code"], record)


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code', 'Title'])
soup = BeautifulSoup(html)
scrape_table(soup)


###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.csa.com/factsheets/supplements/saclass.php')


# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table",width="84%")
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            if (len (table_cells) == 3):
                record['Code'] = table_cells[1].text
                record['Title'] = table_cells[2].text
            else :
                record['Code'] = table_cells[0].text
                record['Title'] = table_cells[1].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Code"], record)


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Code', 'Title'])
soup = BeautifulSoup(html)
scrape_table(soup)


