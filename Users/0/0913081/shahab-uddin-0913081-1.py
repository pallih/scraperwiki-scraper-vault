import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:

    scraperwiki.metadata.save('data_columns', ['Team','Pld','W','D','L','F','A','Diff','Pts'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_st = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_st) == 9:
            record['Team'] = table_st[0].text
            record['Pld'] = table_st[1].text
            record['W'] = table_st[2].text
            record['D'] = table_st[3].text
            record['L'] = table_st[4].text
            record['F'] = table_st[5].text
            record['A'] = table_st[6].text
            record['Diff'] = table_st[7].text
            record['Pts'] = table_st[8].text
            print record,
            print "-------------"
            #Saving the data with the unique key Team:
            scraperwiki.datastore.save(["Team"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://guardian.touch-line.com/?CTID=11&CPID=4&pStr=Comp_Table&t=1"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:

    scraperwiki.metadata.save('data_columns', ['Team','Pld','W','D','L','F','A','Diff','Pts'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_st = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_st) == 9:
            record['Team'] = table_st[0].text
            record['Pld'] = table_st[1].text
            record['W'] = table_st[2].text
            record['D'] = table_st[3].text
            record['L'] = table_st[4].text
            record['F'] = table_st[5].text
            record['A'] = table_st[6].text
            record['Diff'] = table_st[7].text
            record['Pts'] = table_st[8].text
            print record,
            print "-------------"
            #Saving the data with the unique key Team:
            scraperwiki.datastore.save(["Team"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://guardian.touch-line.com/?CTID=11&CPID=4&pStr=Comp_Table&t=1"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
