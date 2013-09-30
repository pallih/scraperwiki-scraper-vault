import scraperwiki
from BeautifulSoup import BeautifulSoup

def journalist(soup):#defining the journalist function
    scraperwiki.metadata.save('data_columns', ['Year','Total killed','Male','Female','Highest country/countries','Number'])#creating table columns list here and it assing some list values and normally list values start from 0
    
    table = soup.find("table", {"class": "in-article sortable"})
     
    rows = table.findAll("tr")#this will find the table rows in the table
    for row in rows:
        record = {}
         
        TableColumns = row.findAll("td")#it will find the table data (rows) 

        if len(TableColumns) ==6:#it will count the length of the function and if the length is equal to 6 only it will record the values
            record['Year'] = TableColumns[0].text
            record['Total killed'] = TableColumns[1].text
            record['Male'] = TableColumns[2].text                  #by using that list values the column will record the perticular value
            record['Female'] = TableColumns[3].text
            record['Highest country/countries'] = TableColumns[4].text
            record['Number'] = TableColumns[5].text
            print record,
            print "----------"
             
            
            scraperwiki.datastore.save(["Year"], record)

web_url="http://www.guardian.co.uk/news/datablog/2010/jan/11/journalists-killed-list-data" #it will the web link

html = scraperwiki.scrape(web_url)#it will assign web link to html
soup = BeautifulSoup(html)#by using that function parameter we can read the values 
journalist(soup) #it will call the journalist function 
import scraperwiki
from BeautifulSoup import BeautifulSoup

def journalist(soup):#defining the journalist function
    scraperwiki.metadata.save('data_columns', ['Year','Total killed','Male','Female','Highest country/countries','Number'])#creating table columns list here and it assing some list values and normally list values start from 0
    
    table = soup.find("table", {"class": "in-article sortable"})
     
    rows = table.findAll("tr")#this will find the table rows in the table
    for row in rows:
        record = {}
         
        TableColumns = row.findAll("td")#it will find the table data (rows) 

        if len(TableColumns) ==6:#it will count the length of the function and if the length is equal to 6 only it will record the values
            record['Year'] = TableColumns[0].text
            record['Total killed'] = TableColumns[1].text
            record['Male'] = TableColumns[2].text                  #by using that list values the column will record the perticular value
            record['Female'] = TableColumns[3].text
            record['Highest country/countries'] = TableColumns[4].text
            record['Number'] = TableColumns[5].text
            print record,
            print "----------"
             
            
            scraperwiki.datastore.save(["Year"], record)

web_url="http://www.guardian.co.uk/news/datablog/2010/jan/11/journalists-killed-list-data" #it will the web link

html = scraperwiki.scrape(web_url)#it will assign web link to html
soup = BeautifulSoup(html)#by using that function parameter we can read the values 
journalist(soup) #it will call the journalist function 
