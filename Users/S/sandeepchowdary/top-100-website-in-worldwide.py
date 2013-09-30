 
import scraperwiki  #this the scraper wiki main source library that scrapes data for me frmo other website
from BeautifulSoup import BeautifulSoup  #this is for tracing the HTML (got by scrape) and to get rows of data

#I have to pass my source url to scrape for getting data

Adplannerhtml = scraperwiki.scrape('http://www.google.com/adplanner/static/top1000/')
print Adplannerhtml                  #I am testing the data by printing

#Now Adplannerhtml contains the HTML of given source URL
##Now I should pass this to BeautifulSoup for tracing and checking the HTML
#So I am passing HTML to BeautifulSoup method provided by BeautifulSoup  Library imported above

ResponseSope = BeautifulSoup(Adplannerhtml) #this will give me soup data

#I am going to create table meta data  

scraperwiki.metadata.save('columns',['Rank', 'Site','Category', 'Unique Visitors', 'Reach', 'Page Views', 'Has Advertising'])       #Table columns are created with this method

#I am using that response soup to get the table and there are many tables in this response soup thats why i am passing 
# unique ID of that table hence it will retuns that single table 

RetrievedTable=ResponseSope .find("table", {"id":"data-table"}) 
print RetrievedTable

#RetrievedTable contains tables rows and we can get those by findAll method

tablerows=RetrievedTable.findAll("tr")

#iterating the loop for each row of table like below
print "Creating Records......."
for tablerow in tablerows:

    record ={}  #Creating new record

    cold=tablerow.findAll("td")  #this will read each cell of row

    if cold:      # checking whether the row is empty or not
        #Fillinf th data
        record['Rank']= int(cold[0].string) #.string will give me the content of that cell#
        #print cold[0].string
        href=cold[1].findAll("a")
        record['Site']=href[1].string
        #print href[1].string
        record['Category']=cold[2].string
        #print cold[2].string
        record['Unique Visitors']=int(cold[3].string.replace(',',''))
        #print cold[3].string
        record['Reach']=float(cold[4].string.replace('%',''))
        #print cold[4].string
        record['Page Views']=int(cold[5].string.replace(',',''))
        #print cold[5].string
        record['Has Advertising']=cold[6].string
        #print cold[6].string
        scraperwiki.datastore.save(["Rank"], record) #saving data to data base
        #print record
print "Creating Records Completed" 
import scraperwiki  #this the scraper wiki main source library that scrapes data for me frmo other website
from BeautifulSoup import BeautifulSoup  #this is for tracing the HTML (got by scrape) and to get rows of data

#I have to pass my source url to scrape for getting data

Adplannerhtml = scraperwiki.scrape('http://www.google.com/adplanner/static/top1000/')
print Adplannerhtml                  #I am testing the data by printing

#Now Adplannerhtml contains the HTML of given source URL
##Now I should pass this to BeautifulSoup for tracing and checking the HTML
#So I am passing HTML to BeautifulSoup method provided by BeautifulSoup  Library imported above

ResponseSope = BeautifulSoup(Adplannerhtml) #this will give me soup data

#I am going to create table meta data  

scraperwiki.metadata.save('columns',['Rank', 'Site','Category', 'Unique Visitors', 'Reach', 'Page Views', 'Has Advertising'])       #Table columns are created with this method

#I am using that response soup to get the table and there are many tables in this response soup thats why i am passing 
# unique ID of that table hence it will retuns that single table 

RetrievedTable=ResponseSope .find("table", {"id":"data-table"}) 
print RetrievedTable

#RetrievedTable contains tables rows and we can get those by findAll method

tablerows=RetrievedTable.findAll("tr")

#iterating the loop for each row of table like below
print "Creating Records......."
for tablerow in tablerows:

    record ={}  #Creating new record

    cold=tablerow.findAll("td")  #this will read each cell of row

    if cold:      # checking whether the row is empty or not
        #Fillinf th data
        record['Rank']= int(cold[0].string) #.string will give me the content of that cell#
        #print cold[0].string
        href=cold[1].findAll("a")
        record['Site']=href[1].string
        #print href[1].string
        record['Category']=cold[2].string
        #print cold[2].string
        record['Unique Visitors']=int(cold[3].string.replace(',',''))
        #print cold[3].string
        record['Reach']=float(cold[4].string.replace('%',''))
        #print cold[4].string
        record['Page Views']=int(cold[5].string.replace(',',''))
        #print cold[5].string
        record['Has Advertising']=cold[6].string
        #print cold[6].string
        scraperwiki.datastore.save(["Rank"], record) #saving data to data base
        #print record
print "Creating Records Completed"