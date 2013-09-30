#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib

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
            #This line didn't work because the links have spaces in them
#            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
#            base_url = 'http://www.horsedeathwatch.com/'
            #These 2 lines test replacing the space in the URL with %20 so it's a working URL
#            testingreplace = (base_url+table_cellsurls[0].attrib.get('href'))
#            print testingreplace.replace(" ", "%20")
 #           horselink = testingreplace.replace(" ", "%20")
            #Use the urllib.urlopen function to open the URL 'properly' so it works
            horselinkurl = urllib.urlopen('http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')).read()
            print horselinkurl
#            horsescrape = scraperwiki.scrape(horselink)
            #Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horselinkurl)
            #put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")
            #print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest3'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib

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
            #This line didn't work because the links have spaces in them
#            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
#            base_url = 'http://www.horsedeathwatch.com/'
            #These 2 lines test replacing the space in the URL with %20 so it's a working URL
#            testingreplace = (base_url+table_cellsurls[0].attrib.get('href'))
#            print testingreplace.replace(" ", "%20")
 #           horselink = testingreplace.replace(" ", "%20")
            #Use the urllib.urlopen function to open the URL 'properly' so it works
            horselinkurl = urllib.urlopen('http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')).read()
            print horselinkurl
#            horsescrape = scraperwiki.scrape(horselink)
            #Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horselinkurl)
            #put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")
            #print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest3'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib

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
            #This line didn't work because the links have spaces in them
#            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
#            base_url = 'http://www.horsedeathwatch.com/'
            #These 2 lines test replacing the space in the URL with %20 so it's a working URL
#            testingreplace = (base_url+table_cellsurls[0].attrib.get('href'))
#            print testingreplace.replace(" ", "%20")
 #           horselink = testingreplace.replace(" ", "%20")
            #Use the urllib.urlopen function to open the URL 'properly' so it works
            horselinkurl = urllib.urlopen('http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')).read()
            print horselinkurl
#            horsescrape = scraperwiki.scrape(horselink)
            #Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horselinkurl)
            #put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")
            #print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest3'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib

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
            #This line didn't work because the links have spaces in them
#            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
#            base_url = 'http://www.horsedeathwatch.com/'
            #These 2 lines test replacing the space in the URL with %20 so it's a working URL
#            testingreplace = (base_url+table_cellsurls[0].attrib.get('href'))
#            print testingreplace.replace(" ", "%20")
 #           horselink = testingreplace.replace(" ", "%20")
            #Use the urllib.urlopen function to open the URL 'properly' so it works
            horselinkurl = urllib.urlopen('http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')).read()
            print horselinkurl
#            horsescrape = scraperwiki.scrape(horselink)
            #Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horselinkurl)
            #put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")
            #print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest3'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
#import the libraries containing our functions
import scraperwiki
import lxml.html
import urllib

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
            #This line didn't work because the links have spaces in them
#            testingreplace = 'http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')
#            base_url = 'http://www.horsedeathwatch.com/'
            #These 2 lines test replacing the space in the URL with %20 so it's a working URL
#            testingreplace = (base_url+table_cellsurls[0].attrib.get('href'))
#            print testingreplace.replace(" ", "%20")
 #           horselink = testingreplace.replace(" ", "%20")
            #Use the urllib.urlopen function to open the URL 'properly' so it works
            horselinkurl = urllib.urlopen('http://www.horsedeathwatch.com/'+table_cellsurls[0].attrib.get('href')).read()
            print horselinkurl
#            horsescrape = scraperwiki.scrape(horselink)
            #Turn the webpage string into an lxml object
            horseroot = lxml.html.fromstring(horselinkurl)
            #put all the <p> tags on the horse page into a list
            pars = horseroot.cssselect("p")
            #print and then store the text_content for the first item <p> in the pars list, the Age
            print pars[0].text_content()
            record['Agetest3'] = pars[0].text_content()
            record['Date'] = table_cells[1].text
            record['Course'] = table_cells[2].text
            #... label 'sales m': the text in the fifth [4] table_cells item...    
            record['Cause of death'] = table_cells[3].text
            # Print out the data we've gathered into the record variable, followed by '-----'
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Horse"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)

# START HERE: define your starting URL - then call a function to scrape it
starting_url = 'http://www.horsedeathwatch.com/'
scrape_and_look_for_next_link(starting_url)
