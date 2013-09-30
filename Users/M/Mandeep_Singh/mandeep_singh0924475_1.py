# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Country', 'All wine, strength','Reported % by vol','Diff.','Red diff','White diff'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_td = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_td) == 6:
            record['Country'] = table_td[0].text
            record['All wine, strength'] = table_td[1].text
            record['Reported % by vol'] = \
            table_td[2].text
            record['Diff.'] = table_td[3].text
            record['Red diff'] = table_td[4].text
            record['White diff'] = table_td[5].text
            print record,
            print "-------------" 
            #Saving the data with the unique key Rank 2009:
            scraperwiki.metadata.save(["Country"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jul/05/wine-strengths-country"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Country', 'All wine, strength','Reported % by vol','Diff.','Red diff','White diff'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_td = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_td) == 6:
            record['Country'] = table_td[0].text
            record['All wine, strength'] = table_td[1].text
            record['Reported % by vol'] = \
            table_td[2].text
            record['Diff.'] = table_td[3].text
            record['Red diff'] = table_td[4].text
            record['White diff'] = table_td[5].text
            print record,
            print "-------------" 
            #Saving the data with the unique key Rank 2009:
            scraperwiki.metadata.save(["Country"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jul/05/wine-strengths-country"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)