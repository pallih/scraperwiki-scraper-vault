import scraperwiki
from BeautifulSoup import BeautifulSoup

#Defining a function
def scraping_data02(soup):
    
#Defining the column names
    scraperwiki.metadata.save('data_columns', ['Constituency', '1997/98', '2008/09', '% change'])
    
#Finding the table in the html code
    table = soup.find("table", {"class": "in-article sortable"}) 
    
#Finding all the rows in the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        
#Finding all the cells in the table
        table_td = row.findAll("td")  

        if len(table_td) == 4:       
            record['Constituency'] = table_td[0].text
            record['1997/98'] = table_td[1].text
            record['2008/09'] = table_td[2].text
            record['% change'] = table_td[3].text
       
 
# Print only the records that satisfy the below condition   
            if table_td[1].txt > 500 and table_td[2].text > 450:
                print record, "-" * 10
            
#Saving with a unique key
            scraperwiki.datastore.save(["Constituency"], record)
  
#Defining the url
url = "http://www.guardian.co.uk/news/datablog/2011/jan/06/university-admissions-constituency"

#Placing the code in a variable called html
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

#Calling the function
scraping_data02(soup)
  
