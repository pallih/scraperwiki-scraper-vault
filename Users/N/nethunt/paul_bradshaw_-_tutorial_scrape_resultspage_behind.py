#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 
#and then BeautifulSoup and scraperwiki to grab the resulting (temporary) results page
#first we need to import those 3 libraries...

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (soup) to scrape - look to see where it is created lower down
def scrape_table(soup):
    #find table class="reports"
    data_table = soup.find("table", { "class" : "reports" })
    #find each table row <tr>
    rows = data_table.findAll("tr")
    #for each row, loop through this
    for row in rows:
        #create a record to hold the data
        record = {}
        #find each cell <td>
        table_cells = row.findAll("td")
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["Name"], record)

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
print "All forms:", [ form.name  for form in br.forms() ]
#as it happens, the name of the form in this page is... "form"
br.select_form(name="form")
#submit the form and put the contents into 'response'
response = br.submit()
#create soup object by reading the contents of response and passing it through BeautifulSoup
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# START scraping by running scrape_table function created above
scrape_table(soup)

#If we wanted to scrape more than one results page we would replace the previous line 
#with this function, which would in turn run the other function
#scrape_and_look_for_next_link(soup)

#if we need to print contents of form so we can see what it contains before next step
#print br.form
#if the form requires certain fields to be filled/selected, then we would do so here
#like so: br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
#see https://scraperwiki.com/scrapers/new/python?template=tutorial-mechanize#
#but we can skip this step and submit this one empty

#If we wanted to assign the 'unpacked' (read) contents of 'response' to new object: 'allschools'
#allschools = response.read()
#print the contents of 'allschools' 
#print allschools

#NEXT: Add to the scraper so it follow the link for each school and grabs data from there
#NEXT: Add to that so that it grabs the linked PDF on each of those
#This scraper grabs the results of an empty search on http://www.isi.net/reports/
#An empty search gives us all the data, but the results page doesn't have its own URL
#So we need to use mechanize to 'submit' that search 
#and then BeautifulSoup and scraperwiki to grab the resulting (temporary) results page
#first we need to import those 3 libraries...

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (soup) to scrape - look to see where it is created lower down
def scrape_table(soup):
    #find table class="reports"
    data_table = soup.find("table", { "class" : "reports" })
    #find each table row <tr>
    rows = data_table.findAll("tr")
    #for each row, loop through this
    for row in rows:
        #create a record to hold the data
        record = {}
        #find each cell <td>
        table_cells = row.findAll("td")
        #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
        if table_cells: 
            record['Name'] = table_cells[0].text
            record['Town'] = table_cells[1].text
            record['Country'] = table_cells[2].text
            record['Year'] = table_cells[3].text
            record['Ages'] = table_cells[4].text
            record['Gender'] = table_cells[5].text
            # Print out the data we've gathered
            print record, '------------'
            # Save the record to the datastore - 'Name' is our unique key - 
            scraperwiki.sqlite.save(["Name"], record)

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
print "All forms:", [ form.name  for form in br.forms() ]
#as it happens, the name of the form in this page is... "form"
br.select_form(name="form")
#submit the form and put the contents into 'response'
response = br.submit()
#create soup object by reading the contents of response and passing it through BeautifulSoup
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# START scraping by running scrape_table function created above
scrape_table(soup)

#If we wanted to scrape more than one results page we would replace the previous line 
#with this function, which would in turn run the other function
#scrape_and_look_for_next_link(soup)

#if we need to print contents of form so we can see what it contains before next step
#print br.form
#if the form requires certain fields to be filled/selected, then we would do so here
#like so: br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
#see https://scraperwiki.com/scrapers/new/python?template=tutorial-mechanize#
#but we can skip this step and submit this one empty

#If we wanted to assign the 'unpacked' (read) contents of 'response' to new object: 'allschools'
#allschools = response.read()
#print the contents of 'allschools' 
#print allschools

#NEXT: Add to the scraper so it follow the link for each school and grabs data from there
#NEXT: Add to that so that it grabs the linked PDF on each of those
