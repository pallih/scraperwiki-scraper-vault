import scraperwiki
import lxml.html

"""
Scraping data from the space weather station. 
We are grabbing data from a table that is updated reguarly on the
space weather site

"""
#first create an auto Primary key for the table
try:
    scraperwiki.sqlite.execute("""
        create table asteroid
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

#scrape the url
html = scraperwiki.scrape("http://www.spaceweather.com/")
root = lxml.html.fromstring(html)

tr = root.cssselect('table.standardText tr') #select all of the tr elements
#print tr

for row in tr:
    record = {}
    ast = row.cssselect('tr td a') #the asteroid name is part of the url in the table
    if ast:
        record['asteroidName'] = ast[0].text_content()
        #print asteroid
    
    cells = row.cssselect('tr td div') #now we can grab the rest of the table
    #print date[1:].text
    if cells:
        astdate = cells[0].text_content()
        if astdate !='Date(UT)':           # the first row in the table we don't need so ask to only record data that hasnt got the column names in
            record['asteroidDate'] = astdate
        astdist = cells[1].text_content()
        if astdist !='Miss Distance':
            record['asteroidDist']= astdist
        astsize = cells[2].text_content()
        if astsize !='Size':
            record['asteroidSize']=astsize
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='asteroid')import scraperwiki
import lxml.html

"""
Scraping data from the space weather station. 
We are grabbing data from a table that is updated reguarly on the
space weather site

"""
#first create an auto Primary key for the table
try:
    scraperwiki.sqlite.execute("""
        create table asteroid
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

#scrape the url
html = scraperwiki.scrape("http://www.spaceweather.com/")
root = lxml.html.fromstring(html)

tr = root.cssselect('table.standardText tr') #select all of the tr elements
#print tr

for row in tr:
    record = {}
    ast = row.cssselect('tr td a') #the asteroid name is part of the url in the table
    if ast:
        record['asteroidName'] = ast[0].text_content()
        #print asteroid
    
    cells = row.cssselect('tr td div') #now we can grab the rest of the table
    #print date[1:].text
    if cells:
        astdate = cells[0].text_content()
        if astdate !='Date(UT)':           # the first row in the table we don't need so ask to only record data that hasnt got the column names in
            record['asteroidDate'] = astdate
        astdist = cells[1].text_content()
        if astdist !='Miss Distance':
            record['asteroidDist']= astdist
        astsize = cells[2].text_content()
        if astsize !='Size':
            record['asteroidSize']=astsize
            scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='asteroid')