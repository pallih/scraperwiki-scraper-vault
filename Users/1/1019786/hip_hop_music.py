import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
    #To distinguish each column by Names:
    scraperwiki.save_var('data_columns', ['Number','Song Title','Artist','Release Year'])
    #Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To identify each cell of the table
        table_flue = row.findAll("td")
        #The number of cells in each row should be five:
        if len(table_flue) == 4:
            record['Number'] = table_flue[0].text
            record['Song Title'] = table_flue[1].text
            record['Artist'] = table_flue[2].text
            record['Release year'] = table_flue[3].text
            print record,
            print "-------------"
            #Saving the data with the unique key Region:
            scraperwiki.sqlite.save(["Number"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jun/13/hip-hop-music-playlist-download"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)