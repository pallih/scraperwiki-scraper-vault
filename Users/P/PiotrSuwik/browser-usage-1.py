###############################################################################
 # Piotr Suwik Scraper - Web browsers usage statistics month by month
 ###############################################################################
 
import scraperwiki
from BeautifulSoup import BeautifulSoup
 
#Define columns
scraperwiki.metadata.save('data_columns', ['Browser', 'Year', 'Month', 'Usage %'])

# retrieve a page
starting_url = 'http://www.w3schools.com/browsers/browsers_stats.asp'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

 # use BeautifulSoup to get all <td> tags
dataTables = soup.find("table",{'class' : 'reference'})
dataTableTrs = dataTables.findAllNext('tr');
id=1
for tr in dataTableTrs:
    #tr.findAllNext(tr)
    #tr.findAllNext('th')
    rows = tr.findAllNext(['td']);
    year = tr.next.next.string
    #print year
    for recordRow in rows:
        id = id+1
        rowToSave = {}
        month = recordRow.string;
        rowToSave['id'] = id;
        ieTD = recordRow.nextSibling.nextSibling;
        rowToSave['IE'] = ieTD.string;
        foTD = ieTD.nextSibling.nextSibling;
        rowToSave['Firefox'] = foTD.string;
        chTD = foTD.nextSibling.nextSibling;
        rowToSave['Chrome'] = chTD.string;
        saTD = chTD.nextSibling.nextSibling;
        rowToSave['Safari'] = saTD.string;
        opTD = saTD.nextSibling.nextSibling;
        rowToSave['Opera'] = opTD.string;

        rowToSave['Year'] = year;
        rowToSave['Month'] = month;
        scraperwiki.datastore.save(["id"], rowToSave)
    
    #record = { "td" : td.text }
    # save records to the datastore
    #scraperwiki.datastore.save(["td"], record)
###############################################################################
 # Piotr Suwik Scraper - Web browsers usage statistics month by month
 ###############################################################################
 
import scraperwiki
from BeautifulSoup import BeautifulSoup
 
#Define columns
scraperwiki.metadata.save('data_columns', ['Browser', 'Year', 'Month', 'Usage %'])

# retrieve a page
starting_url = 'http://www.w3schools.com/browsers/browsers_stats.asp'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

 # use BeautifulSoup to get all <td> tags
dataTables = soup.find("table",{'class' : 'reference'})
dataTableTrs = dataTables.findAllNext('tr');
id=1
for tr in dataTableTrs:
    #tr.findAllNext(tr)
    #tr.findAllNext('th')
    rows = tr.findAllNext(['td']);
    year = tr.next.next.string
    #print year
    for recordRow in rows:
        id = id+1
        rowToSave = {}
        month = recordRow.string;
        rowToSave['id'] = id;
        ieTD = recordRow.nextSibling.nextSibling;
        rowToSave['IE'] = ieTD.string;
        foTD = ieTD.nextSibling.nextSibling;
        rowToSave['Firefox'] = foTD.string;
        chTD = foTD.nextSibling.nextSibling;
        rowToSave['Chrome'] = chTD.string;
        saTD = chTD.nextSibling.nextSibling;
        rowToSave['Safari'] = saTD.string;
        opTD = saTD.nextSibling.nextSibling;
        rowToSave['Opera'] = opTD.string;

        rowToSave['Year'] = year;
        rowToSave['Month'] = month;
        scraperwiki.datastore.save(["id"], rowToSave)
    
    #record = { "td" : td.text }
    # save records to the datastore
    #scraperwiki.datastore.save(["td"], record)
