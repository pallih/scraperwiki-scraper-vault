import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns',['Team','Location','Stadium','Stadium capacity'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "wikitable sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_col = row.findAll("td")
        if table_col:
            record['Team'] = table_col[0].text
            record['Location'] = table_col[1].text
            record['Stadium'] = table_col[2].text
            record['Stadium capacity'] = table_col[3].text
            print record,
            print "-------------"
            #Saving the data with the unique key Team:
            scraperwiki.datastore.save(["Team"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://en.wikipedia.org/wiki/2009%E2%80%9310_Premier_League"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns',['Team','Location','Stadium','Stadium capacity'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "wikitable sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_col = row.findAll("td")
        if table_col:
            record['Team'] = table_col[0].text
            record['Location'] = table_col[1].text
            record['Stadium'] = table_col[2].text
            record['Stadium capacity'] = table_col[3].text
            print record,
            print "-------------"
            #Saving the data with the unique key Team:
            scraperwiki.datastore.save(["Team"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://en.wikipedia.org/wiki/2009%E2%80%9310_Premier_League"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
