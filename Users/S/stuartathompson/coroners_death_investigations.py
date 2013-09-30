import scraperwiki           
import lxml.html #HTML reader
import re #regex
from BeautifulSoup import BeautifulSoup

# Trying to get coroner stats from StatsCan

for x in range(1,2): #1 table for now
    src = 'http://www.statcan.gc.ca/pub/82-214-x/2012001/table-tableau/tbl4-eng.htm' #URL
    html = scraperwiki.scrape(src)
    soup = BeautifulSoup(html) #Get all the html and put into BeautifulSoup
    filter = soup.find('table') #find just the tables
    #print filter
    i = 0 #set up a key for each row
    for row in filter.findAll('tr')[2:]: #get all the rows but skip the first two
        i = i+1
        col = row.findAll({'td'}) #find all cells in this row
        record = { #this iterates through each cell, assigning each value to the corresponding key
            '_dbkey': i,
            'age': col[0].getText(),
            'pei': col[1].getText(),
            'nb': col[2].getText(),
            'qc': col[3].getText(),
            'on': col[4].getText(),
            'sk': col[5].getText(),
            'ab': col[6].getText(),
            'bc': col[7].getText(),
            'yk': col[8].getText(),
            'nwt': col[9].getText(),
            'all': col[9].getText()
        }
        #print record
        scraperwiki.sqlite.save(unique_keys=['_dbkey'], data=record) #save dataimport scraperwiki           
import lxml.html #HTML reader
import re #regex
from BeautifulSoup import BeautifulSoup

# Trying to get coroner stats from StatsCan

for x in range(1,2): #1 table for now
    src = 'http://www.statcan.gc.ca/pub/82-214-x/2012001/table-tableau/tbl4-eng.htm' #URL
    html = scraperwiki.scrape(src)
    soup = BeautifulSoup(html) #Get all the html and put into BeautifulSoup
    filter = soup.find('table') #find just the tables
    #print filter
    i = 0 #set up a key for each row
    for row in filter.findAll('tr')[2:]: #get all the rows but skip the first two
        i = i+1
        col = row.findAll({'td'}) #find all cells in this row
        record = { #this iterates through each cell, assigning each value to the corresponding key
            '_dbkey': i,
            'age': col[0].getText(),
            'pei': col[1].getText(),
            'nb': col[2].getText(),
            'qc': col[3].getText(),
            'on': col[4].getText(),
            'sk': col[5].getText(),
            'ab': col[6].getText(),
            'bc': col[7].getText(),
            'yk': col[8].getText(),
            'nwt': col[9].getText(),
            'all': col[9].getText()
        }
        #print record
        scraperwiki.sqlite.save(unique_keys=['_dbkey'], data=record) #save data