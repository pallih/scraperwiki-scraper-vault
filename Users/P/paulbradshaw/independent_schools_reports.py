#Solves the problem of data being hidden behind a search form
#Does this by using the mechanize library to mimic a browser and store the results of search
#Before scraping the table of search results 

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#create scrape_table function: gets passed an individual page (soup) to scrape 
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

# Scrape page, run scrape_table function
#def scrape_and_look_for_next_link(soup):
 #   scrape_table(soup)

#START HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#If we were using LXML then here's the alternative code
#root = lxml.html.fromstring(response.read())
#see http://www.winningmark.com/2012/03/02/scraperwiki-helping-make-data-more-open/
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping by running function created above, which in turn runs the other function
#scrape_and_look_for_next_link(soup)
scrape_table(soup)


#if we need to print contents of form so we can see what it contains before next step
#print br.form
#if the form requires certain fields to be filled/selected, then we would do so here
#like so: br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
#see https://scraperwiki.com/scrapers/new/python?template=tutorial-mechanize#
#but we can skip this step and submit this one empty

#assign the 'unpacked' (read) contents of 'response' to new object: 'allschools'
#allschools = response.read()
#print the contents of 'allschools' 
#print allschools

#scraping http://www.isi.net/reports/
#Empty search brings up list of schools with links to pages, e.g. http://www.isi.net/schools/6173/
#Each page contains ASPX link to PDF report, e.g. http://reports.isi.net/DownloadReport.aspx?s=6173&t=c
#Source code: <a href="http://reports.isi.net/DownloadReport.aspx?s=6173&t=c" class="blue" target="_blank">View Inspection Report<!-- <span class="grey">&rsaquo;</span>--></a>
#Also link to school info page http://www.isc.co.uk/school_73499.htm
#<p><a href="http://www.isc.co.uk/school_73499.htm" target="_blank" class="view-button">View school information <span class="blue"><strong>&rsaquo;</strong></span></a></p>
#PDF has no numerical data but may be able to extract particular language, e.g. "excellent", "satisfactory"
#One section may be worth scraping specifically:
#Compliance with statutory requirements for children under three
#6.5 The school’s registered provision for childcare meets the requirements of the
#Childcare Act 2006 and no action is required.
#Complaints since the last inspection
#6.6 Since the last inspection, there have been no complaints made to Ofsted that
#required any action to meet national requirements
#Solves the problem of data being hidden behind a search form
#Does this by using the mechanize library to mimic a browser and store the results of search
#Before scraping the table of search results 

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#create scrape_table function: gets passed an individual page (soup) to scrape 
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

# Scrape page, run scrape_table function
#def scrape_and_look_for_next_link(soup):
 #   scrape_table(soup)

#START HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#If we were using LXML then here's the alternative code
#root = lxml.html.fromstring(response.read())
#see http://www.winningmark.com/2012/03/02/scraperwiki-helping-make-data-more-open/
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping by running function created above, which in turn runs the other function
#scrape_and_look_for_next_link(soup)
scrape_table(soup)


#if we need to print contents of form so we can see what it contains before next step
#print br.form
#if the form requires certain fields to be filled/selected, then we would do so here
#like so: br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
#see https://scraperwiki.com/scrapers/new/python?template=tutorial-mechanize#
#but we can skip this step and submit this one empty

#assign the 'unpacked' (read) contents of 'response' to new object: 'allschools'
#allschools = response.read()
#print the contents of 'allschools' 
#print allschools

#scraping http://www.isi.net/reports/
#Empty search brings up list of schools with links to pages, e.g. http://www.isi.net/schools/6173/
#Each page contains ASPX link to PDF report, e.g. http://reports.isi.net/DownloadReport.aspx?s=6173&t=c
#Source code: <a href="http://reports.isi.net/DownloadReport.aspx?s=6173&t=c" class="blue" target="_blank">View Inspection Report<!-- <span class="grey">&rsaquo;</span>--></a>
#Also link to school info page http://www.isc.co.uk/school_73499.htm
#<p><a href="http://www.isc.co.uk/school_73499.htm" target="_blank" class="view-button">View school information <span class="blue"><strong>&rsaquo;</strong></span></a></p>
#PDF has no numerical data but may be able to extract particular language, e.g. "excellent", "satisfactory"
#One section may be worth scraping specifically:
#Compliance with statutory requirements for children under three
#6.5 The school’s registered provision for childcare meets the requirements of the
#Childcare Act 2006 and no action is required.
#Complaints since the last inspection
#6.6 Since the last inspection, there have been no complaints made to Ofsted that
#required any action to meet national requirements
#Solves the problem of data being hidden behind a search form
#Does this by using the mechanize library to mimic a browser and store the results of search
#Before scraping the table of search results 

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#create scrape_table function: gets passed an individual page (soup) to scrape 
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

# Scrape page, run scrape_table function
#def scrape_and_look_for_next_link(soup):
 #   scrape_table(soup)

#START HERE

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.isi.net/reports/'
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
#If we were using LXML then here's the alternative code
#root = lxml.html.fromstring(response.read())
#see http://www.winningmark.com/2012/03/02/scraperwiki-helping-make-data-more-open/
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping by running function created above, which in turn runs the other function
#scrape_and_look_for_next_link(soup)
scrape_table(soup)


#if we need to print contents of form so we can see what it contains before next step
#print br.form
#if the form requires certain fields to be filled/selected, then we would do so here
#like so: br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
#see https://scraperwiki.com/scrapers/new/python?template=tutorial-mechanize#
#but we can skip this step and submit this one empty

#assign the 'unpacked' (read) contents of 'response' to new object: 'allschools'
#allschools = response.read()
#print the contents of 'allschools' 
#print allschools

#scraping http://www.isi.net/reports/
#Empty search brings up list of schools with links to pages, e.g. http://www.isi.net/schools/6173/
#Each page contains ASPX link to PDF report, e.g. http://reports.isi.net/DownloadReport.aspx?s=6173&t=c
#Source code: <a href="http://reports.isi.net/DownloadReport.aspx?s=6173&t=c" class="blue" target="_blank">View Inspection Report<!-- <span class="grey">&rsaquo;</span>--></a>
#Also link to school info page http://www.isc.co.uk/school_73499.htm
#<p><a href="http://www.isc.co.uk/school_73499.htm" target="_blank" class="view-button">View school information <span class="blue"><strong>&rsaquo;</strong></span></a></p>
#PDF has no numerical data but may be able to extract particular language, e.g. "excellent", "satisfactory"
#One section may be worth scraping specifically:
#Compliance with statutory requirements for children under three
#6.5 The school’s registered provision for childcare meets the requirements of the
#Childcare Act 2006 and no action is required.
#Complaints since the last inspection
#6.6 Since the last inspection, there have been no complaints made to Ofsted that
#required any action to meet national requirements
