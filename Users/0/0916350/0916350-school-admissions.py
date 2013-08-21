import scraperwiki
from BeautifulSoup import BeautifulSoup
 
  
  
def scrape_table(soup):
     #In order to differentiate every list by titles:
      scraperwiki.metadata.save('data_columns', ['ID','Place','Reg','% with first preference','% without an offer   from any pref','% one of the three preferences',  '% home apps with an alternative offer', \
      '% apps with offers to a school in another LA'])
      #Recognising the charts in HTML code:
      table = soup.find("table", {"class": "in-article sortable"})
      #In order to pick out every row in the chart:
      rows = table.findAll("tr")
      for row in rows:
          record = {}
          #In order to distinguish every unit of the chart:
          table_td = row.findAll("td")
          #The number of units in every row should be eight:
          if len(table_td) == 8:
              record['ID'] = table_td[0].text
              record[' Place '] = table_td[1].text
              record[' Reg '] = table_td[2].text
              record[' % with first preference '] = table_td[3].text
              record[' % without an offer from any pref'] = table_td[4].text
              record[' % one of the three preferences '] = table_td[5].text
              record[' % home apps with an alternative offer '] = table_td[6].text
              record[' % apps with offers to a school in another LA '] = table_td[7].text
              print record,
              print "-------------"
              #storing the information with the singular key ID:
              scraperwiki.datastore.save(["ID"], record)

#Placing the URL of the world wide web page, From where the information was captured:
website = "http://www.guardian.co.uk/news/datablog/2010/mar/11/school-admissions-choice-places"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
  