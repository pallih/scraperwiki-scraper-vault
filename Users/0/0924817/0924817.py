import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.sqlite.save('data_columns', ['Region', '2000 employment rate',\
          '2009 employment rate ',\
          '2010 CI lower bound employment rate',\
          '2010 Preliminary estimate employment rate',\
          '2010 CI upper bound employment rate'])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 6:#Cross checking
                         record['Region'] = table_td[0].text
                         record['2000 employment rate'] = \
                         table_td[1].text
                         record['2009 employment rate'] = \
                         table_td[2].text
                         record['2010 CI lower bound employment rate '] = \
                         table_td[3].text
                         record['2010 Preliminary estimate employment rate'] = \
                         table_td[4].text
                         record['2010 CI upper bound employment rate'] = \
                         table_td[5].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.sqlite.save(["Region"], record)
#website link
Website = 'http://www.guardian.co.uk/news/datablog/2011/jan/25/global-economy-globalrecession'
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
  