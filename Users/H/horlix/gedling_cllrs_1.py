import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "maindisplayarea" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['A'] = table_cells[0].text
            record['B'] = table_cells[1].text
            record['C'] = table_cells[2].text.rstrip('&nbsp;')
            # Finally, save the record to the datastore
            scraperwiki.datastore.save(["D"], record)
        

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'http://committee-web.gedling.gov.uk/aksgedling/users/public/admin/'
starting_url = base_url + 'main.pl?op=ListCurrentMembers'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_table(soup)
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(soup):
    data_table = soup.find("table", { "class" : "maindisplayarea" })
    rows = data_table.findAll("tr")
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['A'] = table_cells[0].text
            record['B'] = table_cells[1].text
            record['C'] = table_cells[2].text.rstrip('&nbsp;')
            # Finally, save the record to the datastore
            scraperwiki.datastore.save(["D"], record)
        

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'http://committee-web.gedling.gov.uk/aksgedling/users/public/admin/'
starting_url = base_url + 'main.pl?op=ListCurrentMembers'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
scrape_table(soup)
