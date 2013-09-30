import scraperwiki
from BeautifulSoup import BeautifulSoup

#Defining a function
def scraping_data(soup):
    
#Defining the column names
    scraperwiki.metadata.save('data_columns', ['ID', 'Countries', 'Total foreign claims, $m', 'UK', 'US', 'Japan', 'Europe banks total'])
    
#Finding the table in the html code
    table = soup.find("table", {"class": "in-article sortable"}) 
    
#Finding all the rows in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        
#Finding all the cells in the table
        table_td = row.findAll("td")  

        if len(table_td) == 7:       
            record['ID'] = table_td[0].text
            record['Countries'] = table_td[1].text
            record['Total foreign claims, $m'] = table_td[2].text
            record['UK'] = table_td[3].text
            record['US'] = table_td[4].text
            record['Japan'] = table_td[5].text
            record['Europe banks total'] = table_td[6].text
            print record, "-" * 10
            
#Saving with a unique key
            scraperwiki.datastore.save(["Countries"], record)
  
#Defining the url
url = "http://www.guardian.co.uk/news/datablog/2009/nov/30/dubai-financial-crisis-debt-uae-data-world1"

#Placing the code in a variable called html
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

#Calling the function
scraping_data(soup)
  
import scraperwiki
from BeautifulSoup import BeautifulSoup

#Defining a function
def scraping_data(soup):
    
#Defining the column names
    scraperwiki.metadata.save('data_columns', ['ID', 'Countries', 'Total foreign claims, $m', 'UK', 'US', 'Japan', 'Europe banks total'])
    
#Finding the table in the html code
    table = soup.find("table", {"class": "in-article sortable"}) 
    
#Finding all the rows in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        
#Finding all the cells in the table
        table_td = row.findAll("td")  

        if len(table_td) == 7:       
            record['ID'] = table_td[0].text
            record['Countries'] = table_td[1].text
            record['Total foreign claims, $m'] = table_td[2].text
            record['UK'] = table_td[3].text
            record['US'] = table_td[4].text
            record['Japan'] = table_td[5].text
            record['Europe banks total'] = table_td[6].text
            print record, "-" * 10
            
#Saving with a unique key
            scraperwiki.datastore.save(["Countries"], record)
  
#Defining the url
url = "http://www.guardian.co.uk/news/datablog/2009/nov/30/dubai-financial-crisis-debt-uae-data-world1"

#Placing the code in a variable called html
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

#Calling the function
scraping_data(soup)
  
