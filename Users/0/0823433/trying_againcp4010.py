# 
#

import scraperwiki
from BeautifulSoup import BeautifulSoup

my_html = scraperwiki.scrape("http://www.guardian.co.uk/news/datablog/2010/sep/08/worlds-top-100-universities-2010")
#def my_scraper(my_html):
#definition of column name that is going to be stored
scraperwiki.metadata.save('data_columns', ['2010 rank', 'University Name', 'Country', '2009 Rank','2008 Rank'])
    
soup = BeautifulSoup(my_html)
    #find table
rankingTable = soup.find("table", {"class": "stand-alone sortable"})
    
    #find rows of the rankingTable
rows = soup.findAll("td")
for row in rows:
        #declaration of the records 
    records = {}
    cells = row.findAll("tr")
    if cells:
        records['2010 rank'] = cells[0].text
        records['University Name'] = cells[1].text
        records['Country'] = cells[2].text
        records['2009 Rank']= cells[4].text
        records['2008 Rank'] = cells[5].text
        print records, '------------'
            #save the data
        scraperwiki.datastore.save(['University Name'], records)
    
    
#Website - Source - call scrape_table function to process data

#my_scraper(my_html)
#record = { "td" : td.text } # column name and value
#scraperwiki.datastore.save(["td"], record) # save the records one by one