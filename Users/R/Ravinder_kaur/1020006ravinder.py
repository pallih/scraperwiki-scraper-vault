#(Ravinder)This is my scraperwiki

import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.sqlite.get_var('data_columns', ['Team','Team code', 'Team Nationality', 'Team Leader', 'Key Riders', 'Last Year(Best)',])
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
            record['Team'] = table_td[0].text
            record['Team Code'] = table_td[1].text
            record['Team Nationality'] = table_td[2].text
            record['Team Leader'] = table_td[3].text
            record['Key Riders'] = table_td[4].text
            record['Last Year(Best)'] = table_td[5].text
            print record,
            print "----------"
            #Saving the data with the unique key Team 2011:
            scraperwiki.metadata.save(["Team"], record)



#Inserting the URL of the web page, from where the data was taken:
website = 'http://www.guardian.co.uk/news/datablog/2011/jul/01/tour-de-france-cycling-team-list'
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

#(Ravinder)This is my scraperwiki

import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.sqlite.get_var('data_columns', ['Team','Team code', 'Team Nationality', 'Team Leader', 'Key Riders', 'Last Year(Best)',])
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
            record['Team'] = table_td[0].text
            record['Team Code'] = table_td[1].text
            record['Team Nationality'] = table_td[2].text
            record['Team Leader'] = table_td[3].text
            record['Key Riders'] = table_td[4].text
            record['Last Year(Best)'] = table_td[5].text
            print record,
            print "----------"
            #Saving the data with the unique key Team 2011:
            scraperwiki.metadata.save(["Team"], record)



#Inserting the URL of the web page, from where the data was taken:
website = 'http://www.guardian.co.uk/news/datablog/2011/jul/01/tour-de-france-cycling-team-list'
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

