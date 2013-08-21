import scraperwiki
from BeautifulSoup import BeautifulSoup
def scrape_table(soup):

    scraperwiki.metadata.save('data_columns',['rank','web host','price', 'setup','domain','disk space','data transfer','money back','score','hosting review'])
    table = soup.find("table", {"class": "in-article sortable"})
    
    rows = table.findAll("tr")
    for row in rows:

        WHSDetails = {}

    
          
        TableColumns = row.findAll("td")
         
  
        if len(TableColumns) == 10:
              WHSDetails['rank'] = TableColumns[0].text
              WHSDetails['web host'] = TableColumns[1].text
              WHSDetails['price'] = TableColumns[2].text
              WHSDetails['setup'] = TableColumns[3].text
              WHSDetails['domain'] = TableColumns[4].text
              WHSDetails['disk space'] = TableColumns[5].text
              WHSDetails['data transfer'] = TableColumns[6].text
              WHSDetails['money back'] = TableColumns[7].text
              WHSDetails['score'] = TableColumns[8].text
              WHSDetails['hosting review'] = TableColumns[9].text
           
              print record,
              print "-------------"
              #Saving the data with the unique key :
              scraperwiki.datastore.save(["Rank"], record)
   
   
   
dataSource="http://www.webhostingchoice.com/"
html = scraperwiki.scrape(dataSource)
soup = BeautifulSoup(html)
scrape_table(soup)


  
  






