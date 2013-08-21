###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from string import ascii_lowercase

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Zines', 'Title','Issue','Released', 'Publisher','Location','Keywords'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table")
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Title'] = table_cells[0].text
            record['Issue'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Publisher'] = table_cells[3].text
            record['Location'] = table_cells[4].text
            record['Keywords'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Title' is our unique key
            # TODO: Actually title may not be unique, should generate something else
            #   perhaps a combination title-issue 
            scraperwiki.datastore.save(["Title"]+["Issue"], record)
        
# scrape_catalog
def scrape_catalog(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://denverzinelibrary.org/2010/08/21/'
starting_url = base_url + 'catalog-by-title-number/'
scrape_catalog(starting_url)

# next loop thru all of the letters 
for i in ascii_lowercase:
    if i=='k':
        my_url = base_url + 'catalog-by-title' + i + '/'
    else:
        my_url = base_url + 'catalog-by-title-' + i + '/'
    scrape_catalog(my_url)

