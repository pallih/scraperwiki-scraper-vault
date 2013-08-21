import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Rank 2009', \
    'Rank 2008', \
    'Country', \
    'City', \
    'Index 2009'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_td = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_td) == 5:
            record['Rank 2009'] = table_td[0].text
            record['Rank 2008'] = table_td[1].text
            record['Country'] = \
            table_td[2].text
            record['City'] = table_td[3].text
            record['Index 2009'] = table_td[4].text
            print record,
            print "-------------" 
            #Saving the data with the unique key Rank 2009:
            scraperwiki.datastore.save(["Rank 2009"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2009/jul/07/global-economy-economics"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

