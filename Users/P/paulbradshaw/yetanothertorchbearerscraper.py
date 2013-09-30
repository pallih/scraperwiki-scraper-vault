import scraperwiki
import urlparse
import lxml.html

testing = scraperwiki.scrape('http://www.lloydstsblondon2012.co.uk/en/In-your-community/Olympic-Torch-Relay/search/?pg=1')
print testing

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.searchresults tr")  # selects all <tr> blocks within <table class="searchresults">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        ID = 0
        table_cells = row.cssselect("td")
        if table_cells: 
            #need to add URL
            record['Name'] = table_cells[0].text_content
            record['URL'] = table_cells[0].attrib.get('href')
            record['County'] = table_cells[1].text
            record['Category'] = table_cells[2].text
            record['Age'] = table_cells[3].text
            ID =+ 1
            record['ID'] = ID 
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ID"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #store the next link - this is the html we're looking for:
    #<li class="next cta"><a href="/en/In-your-community/Olympic-Torch-Relay/search/?pg=1">Next</a></li></ul>
    next_link = root.cssselect("li.next cta a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


baseurl = 'http://www.lloydstsblondon2012.co.uk'
starting_url = urlparse.urljoin(base_url, '/en/In-your-community/Olympic-Torch-Relay/search/')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html

testing = scraperwiki.scrape('http://www.lloydstsblondon2012.co.uk/en/In-your-community/Olympic-Torch-Relay/search/?pg=1')
print testing

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.searchresults tr")  # selects all <tr> blocks within <table class="searchresults">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        ID = 0
        table_cells = row.cssselect("td")
        if table_cells: 
            #need to add URL
            record['Name'] = table_cells[0].text_content
            record['URL'] = table_cells[0].attrib.get('href')
            record['County'] = table_cells[1].text
            record['Category'] = table_cells[2].text
            record['Age'] = table_cells[3].text
            ID =+ 1
            record['ID'] = ID 
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ID"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #store the next link - this is the html we're looking for:
    #<li class="next cta"><a href="/en/In-your-community/Olympic-Torch-Relay/search/?pg=1">Next</a></li></ul>
    next_link = root.cssselect("li.next cta a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


baseurl = 'http://www.lloydstsblondon2012.co.uk'
starting_url = urlparse.urljoin(base_url, '/en/In-your-community/Olympic-Torch-Relay/search/')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html

testing = scraperwiki.scrape('http://www.lloydstsblondon2012.co.uk/en/In-your-community/Olympic-Torch-Relay/search/?pg=1')
print testing

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.searchresults tr")  # selects all <tr> blocks within <table class="searchresults">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        ID = 0
        table_cells = row.cssselect("td")
        if table_cells: 
            #need to add URL
            record['Name'] = table_cells[0].text_content
            record['URL'] = table_cells[0].attrib.get('href')
            record['County'] = table_cells[1].text
            record['Category'] = table_cells[2].text
            record['Age'] = table_cells[3].text
            ID =+ 1
            record['ID'] = ID 
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ID"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #store the next link - this is the html we're looking for:
    #<li class="next cta"><a href="/en/In-your-community/Olympic-Torch-Relay/search/?pg=1">Next</a></li></ul>
    next_link = root.cssselect("li.next cta a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


baseurl = 'http://www.lloydstsblondon2012.co.uk'
starting_url = urlparse.urljoin(base_url, '/en/In-your-community/Olympic-Torch-Relay/search/')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html

testing = scraperwiki.scrape('http://www.lloydstsblondon2012.co.uk/en/In-your-community/Olympic-Torch-Relay/search/?pg=1')
print testing

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.searchresults tr")  # selects all <tr> blocks within <table class="searchresults">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        ID = 0
        table_cells = row.cssselect("td")
        if table_cells: 
            #need to add URL
            record['Name'] = table_cells[0].text_content
            record['URL'] = table_cells[0].attrib.get('href')
            record['County'] = table_cells[1].text
            record['Category'] = table_cells[2].text
            record['Age'] = table_cells[3].text
            ID =+ 1
            record['ID'] = ID 
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ID"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #store the next link - this is the html we're looking for:
    #<li class="next cta"><a href="/en/In-your-community/Olympic-Torch-Relay/search/?pg=1">Next</a></li></ul>
    next_link = root.cssselect("li.next cta a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


baseurl = 'http://www.lloydstsblondon2012.co.uk'
starting_url = urlparse.urljoin(base_url, '/en/In-your-community/Olympic-Torch-Relay/search/')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html

testing = scraperwiki.scrape('http://www.lloydstsblondon2012.co.uk/en/In-your-community/Olympic-Torch-Relay/search/?pg=1')
print testing

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.searchresults tr")  # selects all <tr> blocks within <table class="searchresults">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        ID = 0
        table_cells = row.cssselect("td")
        if table_cells: 
            #need to add URL
            record['Name'] = table_cells[0].text_content
            record['URL'] = table_cells[0].attrib.get('href')
            record['County'] = table_cells[1].text
            record['Category'] = table_cells[2].text
            record['Age'] = table_cells[3].text
            ID =+ 1
            record['ID'] = ID 
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["ID"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #store the next link - this is the html we're looking for:
    #<li class="next cta"><a href="/en/In-your-community/Olympic-Torch-Relay/search/?pg=1">Next</a></li></ul>
    next_link = root.cssselect("li.next cta a")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)


baseurl = 'http://www.lloydstsblondon2012.co.uk'
starting_url = urlparse.urljoin(base_url, '/en/In-your-community/Olympic-Torch-Relay/search/')
scrape_and_look_for_next_link(starting_url)
