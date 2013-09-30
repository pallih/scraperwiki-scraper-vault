# Blank Python


import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.metadata.save('data_columns''education authority',\
          'school closed or affected',\
          'Total schools ',\
          '%schoolaffected' ])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 4:#Cross checking
                         record['education authority'] = table_td[0].text
                         record['school closed or affected'] = \
                         table_td[1].text
                         record['Total schools'] = \
                         table_td[2].text
                         record['%school affected'] = \
                         table_td[3].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.metadata.save(['education authority'], record)
#website link
Website = "http://www.guardian.co.uk/news/datablog/2011/jun/29/schools-closed-public-sector-strikes"
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
  
# Blank Python


import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.metadata.save('data_columns''education authority',\
          'school closed or affected',\
          'Total schools ',\
          '%schoolaffected' ])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 4:#Cross checking
                         record['education authority'] = table_td[0].text
                         record['school closed or affected'] = \
                         table_td[1].text
                         record['Total schools'] = \
                         table_td[2].text
                         record['%school affected'] = \
                         table_td[3].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.metadata.save(['education authority'], record)
#website link
Website = "http://www.guardian.co.uk/news/datablog/2011/jun/29/schools-closed-public-sector-strikes"
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
  
