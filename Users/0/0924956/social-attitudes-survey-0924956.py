            
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns',['% saying Institution is well run','1983','1986','1987','1994','2009','Change 1983-2009','Change 1994-2009']) 
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_colum = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_colum) == 8:
            record['% saying Institution is well run'] = table_colum[0].text
            record['1983'] = table_colum[1].text
            record['1986'] = table_colum[2].text
            record['1987'] = table_colum[3].text
            record['1994'] = table_colum[4].text
            record['2009'] = table_colum[5].text
            record['Change 1983-2009'] = table_colum[6].text
            record['Change 1994-2009'] = table_colum[7].text
            print record,
            print "-------------"
            #Saving the data with the unique key Well know Institutions:
            scraperwiki.datastore.save(["% saying Institution is well run"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2010/dec/13/social-attitudes-survey-british-data"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
            
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns',['% saying Institution is well run','1983','1986','1987','1994','2009','Change 1983-2009','Change 1994-2009']) 
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_colum = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_colum) == 8:
            record['% saying Institution is well run'] = table_colum[0].text
            record['1983'] = table_colum[1].text
            record['1986'] = table_colum[2].text
            record['1987'] = table_colum[3].text
            record['1994'] = table_colum[4].text
            record['2009'] = table_colum[5].text
            record['Change 1983-2009'] = table_colum[6].text
            record['Change 1994-2009'] = table_colum[7].text
            print record,
            print "-------------"
            #Saving the data with the unique key Well know Institutions:
            scraperwiki.datastore.save(["% saying Institution is well run"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2010/dec/13/social-attitudes-survey-british-data"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
