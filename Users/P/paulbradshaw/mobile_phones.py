# collect the links after <table class="pfDisplayTbl"> <a href
# first page is http://www.carphonewarehouse.com/mobiles/phone-finder

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
    links = root.cssselect("table.pfDisplayTbl a")  # selects all content within <table class="pfDisplayTbl">
    for link in links:
        # Set up our data record - we'll need it later
        print link
        #NEED TO extract the URL
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = link.cssselect("a")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['URL'] = table_cells[0].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.sqlite.save(["URL"], record)

# TO CHECK > "a.pageNext" should be class="pageNext" in HTML - guessing id="pageNext" would be a#pageNext
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
#    next_link = root.cssselect("a")
 #   print next_link
  #  if next_link:
   #     next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
    #    print next_url
     #   scrape_and_look_for_next_link(next_url)


# ...and the extra parameters for the first page of search results
starting_url = 'http://www.carphonewarehouse.com/mobiles/phone-finder'

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)

# collect the links after <table class="pfDisplayTbl"> <a href
# first page is http://www.carphonewarehouse.com/mobiles/phone-finder

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
    links = root.cssselect("table.pfDisplayTbl a")  # selects all content within <table class="pfDisplayTbl">
    for link in links:
        # Set up our data record - we'll need it later
        print link
        #NEED TO extract the URL
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = link.cssselect("a")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['URL'] = table_cells[0].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.sqlite.save(["URL"], record)

# TO CHECK > "a.pageNext" should be class="pageNext" in HTML - guessing id="pageNext" would be a#pageNext
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
#    next_link = root.cssselect("a")
 #   print next_link
  #  if next_link:
   #     next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
    #    print next_url
     #   scrape_and_look_for_next_link(next_url)


# ...and the extra parameters for the first page of search results
starting_url = 'http://www.carphonewarehouse.com/mobiles/phone-finder'

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)

