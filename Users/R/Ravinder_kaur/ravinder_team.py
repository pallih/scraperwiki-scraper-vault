import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.sqlite.save('data_columns', ['Team', 'Team Code','Team Nationality', 
           'Team Leader', 'Key Riders','Last Year (Best)'])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("td")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 6:#Cross checking
                         record['Team'] = table_td[0].text
                         record['Team Code'] = \
                         table_td[1].text
                         record['Team Nationality'] = \
                         table_td[2].text
                         record['Team Leader'] = \
                         table_td[3].text
                         record['Key Riders'] = \
                         table_td[4].text
                         record['Last Year (Best)'] = \
                         table_td[5].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.sqlite.save(["Team"], record)
#website link
Website = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=ravinder_team&query=select%20*%20from%20swdata%20limit%2010'
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
  
