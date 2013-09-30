import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
#To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Country','Overall personal wellbeing','Overall social well-being','Work','Combined wellbeing index'])
#Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
#To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
#To identify each cell of the table
    table_well = row.findAll("td")
#The number of cells in each row should be five:
    if len(table_well) == 5:
        record['Country'] = table_well[0].text
        record['Overall personal wellbeing'] = table_well[1].text
        record['Overall social well-being'] = table_well[2].text
        record['Work'] = table_well[3].text
        record['Combined wellbeing index'] = table_well[4].text
        
        print record,
        print "-------------" * 10
#Saving the data with the unique key Well know Institutions:
        scraperwiki.datastore.save(["Country"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2010/nov/15/happiness-index-wellbeing-nef"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
#To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Country','Overall personal wellbeing','Overall social well-being','Work','Combined wellbeing index'])
#Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
#To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
#To identify each cell of the table
    table_well = row.findAll("td")
#The number of cells in each row should be five:
    if len(table_well) == 5:
        record['Country'] = table_well[0].text
        record['Overall personal wellbeing'] = table_well[1].text
        record['Overall social well-being'] = table_well[2].text
        record['Work'] = table_well[3].text
        record['Combined wellbeing index'] = table_well[4].text
        
        print record,
        print "-------------" * 10
#Saving the data with the unique key Well know Institutions:
        scraperwiki.datastore.save(["Country"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2010/nov/15/happiness-index-wellbeing-nef"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)