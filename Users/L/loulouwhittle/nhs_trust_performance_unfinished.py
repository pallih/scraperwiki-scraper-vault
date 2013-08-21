#INCOMPLETE
# first page is http://www.nhslocal.nhs.uk/perf/search?entype=acute-trust&query=#comp=
# second page is http://www.nhslocal.nhs.uk/perf/search?page=1&entype=acute-trust&query=#comp=
# 3rd page is http://www.nhslocal.nhs.uk/perf/search?page=2&entype=acute-trust&query=#comp=

import scraperwiki
import urlparse
import lxml.html

# This creates a function called scrape_table to scrape specific data from each page passed to it. 

# That data is in between <table> tags - there is only one table on each page so no need to be more specific
# Lower down you'll see it then splits the table into rows, and rows into cells
# It loops through the rows, assigning a record to each, and loops through cells too
# First, here's the creation of the function. 'root' in brackets is the page sent to it
 # - look for 'root' elsewhere in this page to see where it is created
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = row.cssselect("td")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['Title'] = table_cells[0].text
            record['Name'] = table_cells[1].text
            record['Town_of_employment_or_study'] = table_cells[2].text
            record['Registration_number'] = table_cells[3].text
            record['Part_of_the_register'] = table_cells[4].text
            record['Date_of_Registration'] = table_cells[5].text
            record['Info'] = table_cells[6].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.datastore.save(["Registration_number"], record)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("li.pager-next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# establish the base URL... 
base_url = 'http://www.nhslocal.nhs.uk/perf/search?'

# ...and the extra parameters for the first page of search results
starting_url = urlparse.urljoin(base_url, 'entype=acute-trust&query=')

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)



