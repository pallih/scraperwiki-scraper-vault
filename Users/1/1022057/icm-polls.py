import scraperwiki
from BeautifulSoup import BeautifulSoup
print "STARTED RUNNING"
def poll(soup):
#Variable defining
     scraperwiki.metadata.save('data colums',['Election date','CON','LAB','LIB DEN','OTHER','CON LEAD OVER LABOUR','Sample','Fieldwork dates']) 
#To get HTML table
     table = soup.find("table", {"class": "in-article sortable"})
# Table creation
 
     rows = soup.findAll("tr")
     for row in rows:
         record = {}
         #defining rows and colums
         TableColumns = row.findAll("td")

         if len(TableColumns)==8:
                record['Election date'] = TableColumns[0].text
                record['CON'] = TableColumns[1].text
                record['LAB'] = TableColumns[2].text
                record['LIB DEN'] = TableColumns[3].text
                record['OTHER'] = TableColumns[4].text
                record['CON LEAD OVER LABOUR'] = TableColumns[5].text
                record['Sample'] = TableColumns[6].text
                record['fieldwork dates'] = TableColumns[7].text
                print record,
                print "------"
              
# saving data with unique id
                scraperwiki.datastore.save(["Election date"], record)
# defining URL

website="http://www.guardian.co.uk/news/datablog/2009/oct/21/icm-poll-data-labour-conservatives" 

html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
poll(soup)
