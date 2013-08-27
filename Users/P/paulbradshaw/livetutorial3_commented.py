###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Artist'] = table_cells[0].text
            #... label 'album': the text in the second [1] table_cells item...    
            record['Album'] = table_cells[1].text
            #... label 'released': the text in the third [2] table_cells item...    
            record['Released'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    #If there's anything in the variable next_link:
    if next_link:
        #Create a new variable called next_url. Use the urlparse.urljoin function on the variables base_url and next_link - we need to look up the documentation for attrib.get('href') to find out what that does
        print 'WOOHOO', next_link[0].attrib.get('href')
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        #print the contents of that variable next_url
        print next_url
        #run a function called scrape_and_look_for_next_link on the variable next_url
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.madingley.org/uploaded/'
starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Artist'] = table_cells[0].text
            #... label 'album': the text in the second [1] table_cells item...    
            record['Album'] = table_cells[1].text
            #... label 'released': the text in the third [2] table_cells item...    
            record['Released'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    #If there's anything in the variable next_link:
    if next_link:
        #Create a new variable called next_url. Use the urlparse.urljoin function on the variables base_url and next_link - we need to look up the documentation for attrib.get('href') to find out what that does
        print 'WOOHOO', next_link[0].attrib.get('href')
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        #print the contents of that variable next_url
        print next_url
        #run a function called scrape_and_look_for_next_link on the variable next_url
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.madingley.org/uploaded/'
starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Artist'] = table_cells[0].text
            #... label 'album': the text in the second [1] table_cells item...    
            record['Album'] = table_cells[1].text
            #... label 'released': the text in the third [2] table_cells item...    
            record['Released'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    #If there's anything in the variable next_link:
    if next_link:
        #Create a new variable called next_url. Use the urlparse.urljoin function on the variables base_url and next_link - we need to look up the documentation for attrib.get('href') to find out what that does
        print 'WOOHOO', next_link[0].attrib.get('href')
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        #print the contents of that variable next_url
        print next_url
        #run a function called scrape_and_look_for_next_link on the variable next_url
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.madingley.org/uploaded/'
starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Artist'] = table_cells[0].text
            #... label 'album': the text in the second [1] table_cells item...    
            record['Album'] = table_cells[1].text
            #... label 'released': the text in the third [2] table_cells item...    
            record['Released'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    #If there's anything in the variable next_link:
    if next_link:
        #Create a new variable called next_url. Use the urlparse.urljoin function on the variables base_url and next_link - we need to look up the documentation for attrib.get('href') to find out what that does
        print 'WOOHOO', next_link[0].attrib.get('href')
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        #print the contents of that variable next_url
        print next_url
        #run a function called scrape_and_look_for_next_link on the variable next_url
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.madingley.org/uploaded/'
starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(starting_url)
