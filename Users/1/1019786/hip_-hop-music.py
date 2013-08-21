# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Number', \
    'Song Title', \
    'Artist', \
    'Release Year', \
    ])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_td = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_td) == 4:
            record['Number'] = table_td[0].text
            record['Song Title'] = table_td[1].text
            record['Artist'] = \
            table_td[2].text
            record['Release Year'] = table_td[3].text
            print record,
            print "-------------" 
            #Saving the data with the unique key Rank 2009:
            scraperwiki.datastore.save(["Number"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jun/13/hip-hop-music-playlist-download"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)

