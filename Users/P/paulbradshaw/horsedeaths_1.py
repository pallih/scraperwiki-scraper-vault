# An adaptation of Tutorial 2: Basic scraping and saving to the data store.
# This demonstrates how to solve a common problem: empty tags
#NOTE: This scraper would normally also need further development to separate data from different columns

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags as a list - put them in a variable called 'tds' 

#Creating a new variable here solves the unique key problem below...
ID_number = 1

# Save the data in the ScraperWiki datastore.
# For each item in the tds list...
for td in tds:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : td.tag, "td" : td.text, "ID" : ID_number } # column name : value - tag, text, and ID
    scraperwiki.sqlite.save(["ID"], record) # save the records one by one, use ID_Number as unique key
    # An adaptation of Tutorial 2: Basic scraping and saving to the data store.
# This demonstrates how to solve a common problem: empty tags
#NOTE: This scraper would normally also need further development to separate data from different columns

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags as a list - put them in a variable called 'tds' 

#Creating a new variable here solves the unique key problem below...
ID_number = 1

# Save the data in the ScraperWiki datastore.
# For each item in the tds list...
for td in tds:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : td.tag, "td" : td.text, "ID" : ID_number } # column name : value - tag, text, and ID
    scraperwiki.sqlite.save(["ID"], record) # save the records one by one, use ID_Number as unique key
    # An adaptation of Tutorial 2: Basic scraping and saving to the data store.
# This demonstrates how to solve a common problem: empty tags
#NOTE: This scraper would normally also need further development to separate data from different columns

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags as a list - put them in a variable called 'tds' 

#Creating a new variable here solves the unique key problem below...
ID_number = 1

# Save the data in the ScraperWiki datastore.
# For each item in the tds list...
for td in tds:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : td.tag, "td" : td.text, "ID" : ID_number } # column name : value - tag, text, and ID
    scraperwiki.sqlite.save(["ID"], record) # save the records one by one, use ID_Number as unique key
    # An adaptation of Tutorial 2: Basic scraping and saving to the data store.
# This demonstrates how to solve a common problem: empty tags
#NOTE: This scraper would normally also need further development to separate data from different columns

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags as a list - put them in a variable called 'tds' 

#Creating a new variable here solves the unique key problem below...
ID_number = 1

# Save the data in the ScraperWiki datastore.
# For each item in the tds list...
for td in tds:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : td.tag, "td" : td.text, "ID" : ID_number } # column name : value - tag, text, and ID
    scraperwiki.sqlite.save(["ID"], record) # save the records one by one, use ID_Number as unique key
    # An adaptation of Tutorial 2: Basic scraping and saving to the data store.
# This demonstrates how to solve a common problem: empty tags
#NOTE: This scraper would normally also need further development to separate data from different columns

import scraperwiki
html = scraperwiki.scrape('http://www.horsedeathwatch.com/')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags as a list - put them in a variable called 'tds' 

#Creating a new variable here solves the unique key problem below...
ID_number = 1

# Save the data in the ScraperWiki datastore.
# For each item in the tds list...
for td in tds:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : td.tag, "td" : td.text, "ID" : ID_number } # column name : value - tag, text, and ID
    scraperwiki.sqlite.save(["ID"], record) # save the records one by one, use ID_Number as unique key
    