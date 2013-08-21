import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.sqlite.save('data_columns', ['Authority', 'Avg sync speed (Mbit/s)',\
          ' % not rece - iving 2Mbit/s ',\
          'Super fast broad - band availa - bility (%)','Take -up (excluding super - fast broad - band) (%)','Overall score'])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 6:#Cross checking
                         record['Authority'] = table_td[0].text
                                              
                         record['Overall score'] = table_td[5].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.sqlite.save(["Authority"], record)
#website link
Website = 'http://www.guardian.co.uk/news/datablog/2011/jul/06/uk-broadband-internet-speed-by-area'
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
  