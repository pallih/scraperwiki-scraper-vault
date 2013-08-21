import scraperwiki
import urlparse
import lxml.html
import mechanize

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Horse'] = table_cells[0].text_content()
            #... label 'album': the text in the second [1] table_cells item...    
            table_cellsurls = table_cells[0].cssselect("a")
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.london2012.com/join-in/whats-on/#'
#set the URL containing the form we need to open with mechanize
#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
br.open(starting_url)
#find out and display (print) the names of any forms in the HTML
#i.e. <form ... name="
print "All forms:", [ form.name for form in br.forms() ]
#as it happens, the name of the form in this page is... "form"
br.select_form(name="form")
#submit the form and put the contents into 'response'
response = br.submit()
#read contents of 'response' and print
#print response.read()
#read contents of 'response' and put into 'html'
html = response.read()
print html
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)
import scraperwiki
import urlparse
import lxml.html
import mechanize

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Horse'] = table_cells[0].text_content()
            #... label 'album': the text in the second [1] table_cells item...    
            table_cellsurls = table_cells[0].cssselect("a")
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.london2012.com/join-in/whats-on/#'
#set the URL containing the form we need to open with mechanize
#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
br.open(starting_url)
#find out and display (print) the names of any forms in the HTML
#i.e. <form ... name="
print "All forms:", [ form.name for form in br.forms() ]
#as it happens, the name of the form in this page is... "form"
br.select_form(name="form")
#submit the form and put the contents into 'response'
response = br.submit()
#read contents of 'response' and print
#print response.read()
#read contents of 'response' and put into 'html'
html = response.read()
print html
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)
import scraperwiki
import urlparse
import lxml.html
import mechanize

# scrape_table function: gets passed an individual page to scrape
def scrape_table(elephant):
    rows = elephant.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        #if there's anything in the table_cells variable (a list)
        if table_cells: 
            #add to the variable record (a dictionary) these pairs: label 'artist': the text in the first [0] table_cells item...
            record['Horse'] = table_cells[0].text_content()
            #... label 'album': the text in the second [1] table_cells item...    
            table_cellsurls = table_cells[0].cssselect("a")
            record['HorseURL'] = table_cellsurls[0].attrib.get('href')
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.london2012.com/join-in/whats-on/#'
#set the URL containing the form we need to open with mechanize
#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
br.open(starting_url)
#find out and display (print) the names of any forms in the HTML
#i.e. <form ... name="
print "All forms:", [ form.name for form in br.forms() ]
#as it happens, the name of the form in this page is... "form"
br.select_form(name="form")
#submit the form and put the contents into 'response'
response = br.submit()
#read contents of 'response' and print
#print response.read()
#read contents of 'response' and put into 'html'
html = response.read()
print html
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)
