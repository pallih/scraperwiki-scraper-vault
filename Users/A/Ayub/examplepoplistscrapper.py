#Example
import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.sqlite.save('data_columns', ['Number', 'Song title',\
          'Artist ',\
          'Release year'])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 4:#Cross checking
                         record['Number'] = table_td[0].text
                         record['Song title'] = \
                         table_td[1].text
                         record['Artist'] = \
                         table_td[2].text
                         record['Release year'] = \
                         table_td[3].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.sqlite.save(["Number"], record)
#website link
Website = 'http://www.guardian.co.uk/news/datablog/2011/jun/11/pop-music-playlist-download'
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
#Example
import scraperwiki
from BeautifulSoup import BeautifulSoup
 
def scrape_table(soup):
          #to define coloumns name used in table
          scraperwiki.sqlite.save('data_columns', ['Number', 'Song title',\
          'Artist ',\
          'Release year'])
          table = soup.find("table", {"class": "in-article sortable"})
          #To each row of table is selected
          rows = table.findAll("tr")
          for row in rows:
                 record = {}
                 #To select table row cells
                 table_td = row.findAll("td")
                 #Each row include six cells
                 if len(table_td) == 4:#Cross checking
                         record['Number'] = table_td[0].text
                         record['Song title'] = \
                         table_td[1].text
                         record['Artist'] = \
                         table_td[2].text
                         record['Release year'] = \
                         table_td[3].text
                         print record,
                         print "-" * 10
                         #Save data step by step
                         scraperwiki.sqlite.save(["Number"], record)
#website link
Website = 'http://www.guardian.co.uk/news/datablog/2011/jun/11/pop-music-playlist-download'
html = scraperwiki.scrape(Website)
soup = BeautifulSoup(html)
scrape_table(soup)
