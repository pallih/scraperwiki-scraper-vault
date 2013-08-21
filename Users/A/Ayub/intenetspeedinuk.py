import scraperwiki
from BeautifulSoup import BeautifulSoup


def scrape_table(soup):
#To distinguish each column by Names:
    scraperwiki.metadata.save('data_columns', ['Authority','Avg sync speed (Mbit/s)','Super fast broad - band availa - bility (%)','Take -up (excluding super - fast broad - band) (%)','Overall score'])
#Identifying the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
#To identify each row of the table:
    rows = table.findAll("tr")
    for row in rows:
        record = {}
#To identify each cell of the table
    table_speed = row.findAll("td")
#The number of cells in each row should be five:
    if len(table_speed) == 5:
        record['Authority'] = table_speed[0].text
        record['Avg sync speed (Mbit/s)'] = table_speed[1].text
        record['Super fast broad - band availa - bility (%)'] = table_speed[2].text
        record['Take -up (excluding super - fast broad - band) (%)'] = table_speed[3].text
        record['Overall score'] = table_speed[4].text
        
        print record,
        print "-------------" * 10
#Saving the data with the unique key Well know Institutions:
        scraperwiki.datastore.save(["Authority"], record)


#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jul/06/uk-broadband-internet-speed-by-area"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
