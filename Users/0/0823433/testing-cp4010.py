# **********************************************************************
# This is part of my portfolio for CP4010
# Name: Olubukola Sokunbi
# Student Number: 0823433
# This 
# **********************************************************************

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.ucas.com/students/choosingcourses/choosinguni/instguide/')
print html

# scraperwiki.metadata.save('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

table_scrape = BeautifulSoup(html)

tables = table_scrape.find("table", {"class": "stand-alone sortable"}) # get all the <td> tags


rows = tables.findAll(tr)
for td in tables:
    print td # the full HTML tag
    print td.text # just the text inside the HTML tag

for row in rows:
        #declaration of the records 
        records = {}
        cells = row.findAll("td")
        if cells:
            records['University'] = cells[0].text
            records['2'] = cells[1].text
            records['3'] = cells[2].text
            records['4']= cells[3].text
            #records[5'] = cells[4].text
            print records, '------------'
            #save the data
            scraperwiki.datastore.save(['University'], records)


    # record = { "td" : td.text } # column name and value
    # scraperwiki.datastore.save(["td"], record) # save the records one by one















# 
#

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.timeshighereducation.co.uk/world-university-rankings/2010-2011/top-200.html')
soup = BeautifulSoup(html)
def my_scraper(soup):
#definition of column name that is going to be stored
    scraperwiki.metadata.save('data_columns', ['WORLD RANK', 'INSTITUTION', 'COUNTRY / REGION', 'OVERALL SCORE'])
    
    
    #find table
    rankingTable = soup.find("table", {"class": "stand-alone sortable"})

#tables = table_scrape.find("table", {"class": "stand-alone sortable"})
    
    #find rows of the rankingTable
    rows = soup.findAll("tr")
    for row in rows:
        #declaration of the records 
        record = {}
        cells = row.findAll("td")
        if cells:
            record['WORLD RANK'] = cells[1].text
            record['INSTITUTION'] = cells[2].text
            record['COUNTRY / REGION'] = cells[3].text
            record['OVERALL SCORE']= cells[4].text
            #records['Score'] = cells[11].text
            print record
            
            #save the data
        #scraperwiki.datastore.save(['Rank'], records)
#for td in rows:
        #record = { "td" : td.text } # column name and value
        
        
            scraperwiki.datastore.save(['WORLD RANK'], record) # save the records one by one
    
#Website - Source - call scrape_table function to process data

my_scraper(soup)