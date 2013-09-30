import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['Clinician', 'Location', 'CurrentRecognitions'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "id" : "ProviderSearchResultsTable1_ProvidersGrid" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Clinician'] = table_cells[0].text
            record['Location'] = table_cells[1].text
            record['CurrentRecognitions'] = table_cells[2].text.rstrip('&nbsp;')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Day' is our unique key
            scraperwiki.sqlite.save(["Clinician"], record)
        
# 'scrape_and_look_for_next_link' function: scrapes links on page, then
# hunts for a 'next' link: if one is found, calls itself recursively
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
    if next_link:
        # okay, following the 'next' link actually means submitting a form...
        br.select_form(name='ctl00')
        br.form.set_all_readonly(False) # allow changing the .value of all controls
        # set the ASP.NET fields
        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
        br['__EVENTARGUMENT'] = ''
        br.submit()
        soup = BeautifulSoup(br.response().read())
        #print soup
        scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: begin with the first page of links
# ---------------------------------------------------------------------------

base_url = 'http://recognition.ncqa.org/'
starting_url = base_url + 'PSearchResults.aspx?state=ME&rp='
br = mechanize.Browser()
# Fake the user-agent - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
#print soup # check the HTML is OK
# start scraping
scrape_and_look_for_next_link(soup)
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['Clinician', 'Location', 'CurrentRecognitions'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table", { "id" : "ProviderSearchResultsTable1_ProvidersGrid" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells: 
            record['Clinician'] = table_cells[0].text
            record['Location'] = table_cells[1].text
            record['CurrentRecognitions'] = table_cells[2].text.rstrip('&nbsp;')
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Day' is our unique key
            scraperwiki.sqlite.save(["Clinician"], record)
        
# 'scrape_and_look_for_next_link' function: scrapes links on page, then
# hunts for a 'next' link: if one is found, calls itself recursively
def scrape_and_look_for_next_link(soup):
    scrape_table(soup)
    next_link = soup.find("a", { "id" : "ProviderSearchResultsTable1_NextLinkButton" })
    if next_link:
        # okay, following the 'next' link actually means submitting a form...
        br.select_form(name='ctl00')
        br.form.set_all_readonly(False) # allow changing the .value of all controls
        # set the ASP.NET fields
        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
        br['__EVENTARGUMENT'] = ''
        br.submit()
        soup = BeautifulSoup(br.response().read())
        #print soup
        scrape_and_look_for_next_link(soup)

# ---------------------------------------------------------------------------
# START HERE: begin with the first page of links
# ---------------------------------------------------------------------------

base_url = 'http://recognition.ncqa.org/'
starting_url = base_url + 'PSearchResults.aspx?state=ME&rp='
br = mechanize.Browser()
# Fake the user-agent - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
#print soup # check the HTML is OK
# start scraping
scrape_and_look_for_next_link(soup)
