import scraperwiki
from BeautifulSoup import BeautifulSoup

 
 
def scrape_table(soup):
    
     scraperwiki.metadata.save('data_columns', ['Name','Job Title','Organisation','Annual pay rate - including taxable benefits and allowances'])
     #Identifying the tables in HTML code:
     table = soup.find("table", {"class": "in-article sortable"})
     #To identify each row of the table:
     rows = table.findAll("tr")
     for row in rows:
         record = {}
         
         table_td = row.findAll("td")
         
         if len(table_td) == 4:
             record['Name'] = table_td[0].text
             record[' Job Title '] = table_td[1].text
             record[' Organisation '] = table_td[2].text
             record[' Annual pay rate - including taxable benefits and allowances '] = table_td[3].text
             
             print record,
             print "-------------"
             #Saving the data with the unique key ID:
             scraperwiki.datastore.save(["Name"], record)

#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2010/may/31/senior-civil-servants-salaries-data"
html = scraperwiki.scrape(website)
soup = BeautifulSoup(html)
scrape_table(soup)
