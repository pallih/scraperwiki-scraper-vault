#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 


#import libraries
import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Name'] = table_cells[0].text_content()
            record['Town'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno++
            record['ID'] = idno 
            record['Country'] = table_cells[2].text_content()
            record['Year'] = table_cells[3].text_content()
            record['Ages'] = table_cells[4].text_content()
            record['Gender'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)
#This function isn't needed as all our results are on one page
#But if they were on a series of page, this would scrape the first page, running scrape_table function
#then find the 'next' link and repeat the process on that, etc. Here is the start of that function:
#def scrape_and_look_for_next_link(soup):
#    scrape_table(soup)

#SCRAPER PROPER STARTS HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)

#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 


#import libraries
import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Name'] = table_cells[0].text_content()
            record['Town'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno++
            record['ID'] = idno 
            record['Country'] = table_cells[2].text_content()
            record['Year'] = table_cells[3].text_content()
            record['Ages'] = table_cells[4].text_content()
            record['Gender'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)
#This function isn't needed as all our results are on one page
#But if they were on a series of page, this would scrape the first page, running scrape_table function
#then find the 'next' link and repeat the process on that, etc. Here is the start of that function:
#def scrape_and_look_for_next_link(soup):
#    scrape_table(soup)

#SCRAPER PROPER STARTS HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)

#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 


#import libraries
import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Name'] = table_cells[0].text_content()
            record['Town'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno++
            record['ID'] = idno 
            record['Country'] = table_cells[2].text_content()
            record['Year'] = table_cells[3].text_content()
            record['Ages'] = table_cells[4].text_content()
            record['Gender'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)
#This function isn't needed as all our results are on one page
#But if they were on a series of page, this would scrape the first page, running scrape_table function
#then find the 'next' link and repeat the process on that, etc. Here is the start of that function:
#def scrape_and_look_for_next_link(soup):
#    scrape_table(soup)

#SCRAPER PROPER STARTS HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)

#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 


#import libraries
import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Name'] = table_cells[0].text_content()
            record['Town'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno++
            record['ID'] = idno 
            record['Country'] = table_cells[2].text_content()
            record['Year'] = table_cells[3].text_content()
            record['Ages'] = table_cells[4].text_content()
            record['Gender'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)
#This function isn't needed as all our results are on one page
#But if they were on a series of page, this would scrape the first page, running scrape_table function
#then find the 'next' link and repeat the process on that, etc. Here is the start of that function:
#def scrape_and_look_for_next_link(soup):
#    scrape_table(soup)

#SCRAPER PROPER STARTS HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)

#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 


#import libraries
import scraperwiki
import mechanize
import lxml.html
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (root) to scrape - look to see where it is created lower down
def scrape_table(root):
    #grab all table rows <tr> in table class="reports"
    rows = root.cssselect("tr")
    #create an ID number set at 0 - will add 1 every time we store a record (below)
    idno = 0
    #for each row, loop through this
    #create a record to hold the data
    record = {}
    for row in rows:
        #create a list of all cells <td> in that row
        table_cells = row.cssselect("td")
        if table_cells: 
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            record['Name'] = table_cells[0].text_content()
            record['Town'] = table_cells[1].text_content()
            #this line adds 1 to the ID no. we set at 0 earlier
            idno++
            record['ID'] = idno 
            record['Country'] = table_cells[2].text_content()
            record['Year'] = table_cells[3].text_content()
            record['Ages'] = table_cells[4].text_content()
            record['Gender'] = table_cells[5].text_content()
            #find any links <a ...
            table_cellsurls = table_cells[0].cssselect("a")
            #grab the href=" attribute of the first <a ... and store
            record['URL'] = table_cellsurls[0].attrib.get('href')
                # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["ID"], record)
#This function isn't needed as all our results are on one page
#But if they were on a series of page, this would scrape the first page, running scrape_table function
#then find the 'next' link and repeat the process on that, etc. Here is the start of that function:
#def scrape_and_look_for_next_link(soup):
#    scrape_table(soup)

#SCRAPER PROPER STARTS HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#ERROR GENERATED: XMLSyntaxError: None
root = lxml.html.fromstring(html)

# START scraping by running scrape_table function created above
scrape_table(root)

