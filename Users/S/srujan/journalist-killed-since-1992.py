import scraperwiki
from Beautifulsoup import Beautifulsoap

def scrape_table(soup):
    scraperwiki.metadata.save('data_columns', ['Year','Total_killed','Male','Female','Highest country/countries','Number',])
    
    table = soup.find("table", {"class": "in-article sortable"})
     
    rows = table.findAll("tr")
    for rows in rows:
        record = {}
         
        table_td = row.findAll("td")

        if len(table_td) ==5:
            record['Year'] = table_td[0].text
            record['Total_killed'] = table_td[1].text
            record['Male'] = table_td[2].text
            record['Female'] = table_td[3].text
            record['Highest country/countries'] = table_td[4].text
            record['Number'] = table_td[5].text
            print record,
             
            
            scraperwiki.datastore.save(["Year"], record)

website = "http://www.guardian.co.uk/news/datablog/2010/jan/11/journalists-killed-list-data"

html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
import scraperwiki
from Beautifulsoup import Beautifulsoap

def scrape_table(soup):
    scraperwiki.metadata.save('data_columns', ['Year','Total_killed','Male','Female','Highest country/countries','Number',])
    
    table = soup.find("table", {"class": "in-article sortable"})
     
    rows = table.findAll("tr")
    for rows in rows:
        record = {}
         
        table_td = row.findAll("td")

        if len(table_td) ==5:
            record['Year'] = table_td[0].text
            record['Total_killed'] = table_td[1].text
            record['Male'] = table_td[2].text
            record['Female'] = table_td[3].text
            record['Highest country/countries'] = table_td[4].text
            record['Number'] = table_td[5].text
            print record,
             
            
            scraperwiki.datastore.save(["Year"], record)

website = "http://www.guardian.co.uk/news/datablog/2010/jan/11/journalists-killed-list-data"

html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
