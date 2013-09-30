###############################################################################
# Scraper designed to interrogate the Committee feed page of CoLC website
# and pull all information back into the Scraperwiki datastore for
# future reference
###############################################################################


#Set up the scraper
import scraperwiki
from BeautifulSoup import BeautifulSoup

#Set up our data store elements
scraperwiki.metadata.save('data_columns', ['Date', 'Event', 'Link', 'Title'])

#Retrieve our page
starting_url = 'http://tmf.lincoln.gov.uk/Whatsnew.aspx?sec_id=3202'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

#Find the data we want to use in the page by looking for the table ID; we're then making
#an array of all the rows in that table

datatable = soup.find("table", { "id": "ctl00_cph1_dgResult" } )
rows = datatable.findAll("tr")
#print rows



#Now we're going to interrogate each row
for row in rows:
    record = {}
    table_cells = row.findAll("td")
    #print table_cells
    
    #First, let's set up and insert the data into the data store

    if table_cells:
        link = table_cells[2].find('a');        

        #We're going to hack together a new date to get rid of the ordinal (th, rd etc)

        date_rest = table_cells[0].text[4:]
        date_day_pre = table_cells[0].text[:4]

        date_day = date_day_pre.rstrip('thrdstn ')

        record['Date'] = date_day + ' ' + date_rest.lstrip()
        record['Title'] = table_cells[2].text
        record['Event'] = table_cells[1].text
        record['Link'] = 'http://tmf.lincoln.gov.uk/' + link['href']

        print record

        #We're done; save the record...
        scraperwiki.datastore.save(["Title"], record)###############################################################################
# Scraper designed to interrogate the Committee feed page of CoLC website
# and pull all information back into the Scraperwiki datastore for
# future reference
###############################################################################


#Set up the scraper
import scraperwiki
from BeautifulSoup import BeautifulSoup

#Set up our data store elements
scraperwiki.metadata.save('data_columns', ['Date', 'Event', 'Link', 'Title'])

#Retrieve our page
starting_url = 'http://tmf.lincoln.gov.uk/Whatsnew.aspx?sec_id=3202'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

#Find the data we want to use in the page by looking for the table ID; we're then making
#an array of all the rows in that table

datatable = soup.find("table", { "id": "ctl00_cph1_dgResult" } )
rows = datatable.findAll("tr")
#print rows



#Now we're going to interrogate each row
for row in rows:
    record = {}
    table_cells = row.findAll("td")
    #print table_cells
    
    #First, let's set up and insert the data into the data store

    if table_cells:
        link = table_cells[2].find('a');        

        #We're going to hack together a new date to get rid of the ordinal (th, rd etc)

        date_rest = table_cells[0].text[4:]
        date_day_pre = table_cells[0].text[:4]

        date_day = date_day_pre.rstrip('thrdstn ')

        record['Date'] = date_day + ' ' + date_rest.lstrip()
        record['Title'] = table_cells[2].text
        record['Event'] = table_cells[1].text
        record['Link'] = 'http://tmf.lincoln.gov.uk/' + link['href']

        print record

        #We're done; save the record...
        scraperwiki.datastore.save(["Title"], record)