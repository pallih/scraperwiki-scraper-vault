# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    #each column from the table is defined in the below function:
    scraperwiki.metadata.save('data_columns', ['order','Area of usual residence','2009,number','2009,rate','2001,number','2001,rate'])
    #the table here is defind as in the website and also the  class is defined:
    table = soup.find("table", {"class": "in-article sortable"})
    #the rows are defind as in the table:
    rows = table.findAll("tr")
    for ro in rows:
        record = {}
        #the cells in the row is defined in the below function
        table_preg = ro.findAll("td")
        #the total number of rows are 6 which are defined in the below function:
        if len(table_preg) == 6:
            record['order'] = table_preg[0].text
            record['Area of usual residence'] = table_preg[1].text
            record['2009,number'] = table_preg[2].text
            record['2009,rate'] = table_preg[3].text
            record['2001,number'] = table_preg[4].text
            record['2001,rate'] = table_preg[5].text
            print record,
            print "-------------"
            #the extracted data is saved by the order for which the below function is written:
            scraperwiki.datastore.save(["order"], record)

# below is the link from which the data is extrected and shown in the scrapper.
website = "http://www.guardian.co.uk/news/datablog/2011/feb/22/teenage-pregnancy-rates-england-wales-map"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    #each column from the table is defined in the below function:
    scraperwiki.metadata.save('data_columns', ['order','Area of usual residence','2009,number','2009,rate','2001,number','2001,rate'])
    #the table here is defind as in the website and also the  class is defined:
    table = soup.find("table", {"class": "in-article sortable"})
    #the rows are defind as in the table:
    rows = table.findAll("tr")
    for ro in rows:
        record = {}
        #the cells in the row is defined in the below function
        table_preg = ro.findAll("td")
        #the total number of rows are 6 which are defined in the below function:
        if len(table_preg) == 6:
            record['order'] = table_preg[0].text
            record['Area of usual residence'] = table_preg[1].text
            record['2009,number'] = table_preg[2].text
            record['2009,rate'] = table_preg[3].text
            record['2001,number'] = table_preg[4].text
            record['2001,rate'] = table_preg[5].text
            print record,
            print "-------------"
            #the extracted data is saved by the order for which the below function is written:
            scraperwiki.datastore.save(["order"], record)

# below is the link from which the data is extrected and shown in the scrapper.
website = "http://www.guardian.co.uk/news/datablog/2011/feb/22/teenage-pregnancy-rates-england-wales-map"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
