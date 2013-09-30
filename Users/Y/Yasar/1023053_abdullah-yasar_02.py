import scraperwiki
from BeautifulSoup import BeautifulSoup

#Defining a function
def scraping_data01(soup):
    
#Defining the column names
    scraperwiki.metadata.save('data_columns', ['LA name', 'Ave spending per pupil, secondary school, £', '% with 5+ A*-C grades inc. English & Mathematics GCSEs, 2009/10', '% with 2 or more passes of A Level equivalent size'])
    
#Finding the table in the html code
    table = soup.find("table", {"class": "in-article sortable"}) 
    
#Finding all the rows in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        
#Finding all the cells in the table
        table_td = row.findAll("td")  

        if len(table_td) == 4:       
            record['LA name'] = table_td[0].text
            record['Ave spending per pupil, secondary school, £'] = table_td[1].text
            record['% with 5+ A*-C grades inc. English & Mathematics GCSEs, 2009/10'] = table_td[2].text
            record['% with 2 or more passes of A Level equivalent size'] = table_td[3].text
       
 
# Print only the records whose value is greater than 40   
            if table_td[2].txt > 40:
                print record, "-" * 10
            
#Saving with a unique key
            scraperwiki.datastore.save(["LA name"], record)
  
#Defining the url
url = "http://www.guardian.co.uk/news/datablog/2011/jan/12/secondary-school-tables-gcse-alevel-data"

#Placing the code in a variable called html
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

#Calling the function
scraping_data01(soup)
  
import scraperwiki
from BeautifulSoup import BeautifulSoup

#Defining a function
def scraping_data01(soup):
    
#Defining the column names
    scraperwiki.metadata.save('data_columns', ['LA name', 'Ave spending per pupil, secondary school, £', '% with 5+ A*-C grades inc. English & Mathematics GCSEs, 2009/10', '% with 2 or more passes of A Level equivalent size'])
    
#Finding the table in the html code
    table = soup.find("table", {"class": "in-article sortable"}) 
    
#Finding all the rows in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        
#Finding all the cells in the table
        table_td = row.findAll("td")  

        if len(table_td) == 4:       
            record['LA name'] = table_td[0].text
            record['Ave spending per pupil, secondary school, £'] = table_td[1].text
            record['% with 5+ A*-C grades inc. English & Mathematics GCSEs, 2009/10'] = table_td[2].text
            record['% with 2 or more passes of A Level equivalent size'] = table_td[3].text
       
 
# Print only the records whose value is greater than 40   
            if table_td[2].txt > 40:
                print record, "-" * 10
            
#Saving with a unique key
            scraperwiki.datastore.save(["LA name"], record)
  
#Defining the url
url = "http://www.guardian.co.uk/news/datablog/2011/jan/12/secondary-school-tables-gcse-alevel-data"

#Placing the code in a variable called html
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

#Calling the function
scraping_data01(soup)
  
