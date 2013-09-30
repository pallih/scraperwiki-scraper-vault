                                                                                            import scraperwiki,re
from BeautifulSoup import BeautifulSoup

print "Sachin Tendulkar Oneday Centuries List"
#Get the HTML Page
Gethtml = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_international_cricket_centuries_by_Sachin_Tendulkar')
#Get the Source Code for the Web Page
Bsoup = BeautifulSoup(Gethtml )
#Save the Required Informaiton in the Data Columns with Column names
scraperwiki.metadata.save('data_columns', ['No.','Score', 'Against','Inn.','Test', 'Venue','H/A','Date','Result'])
#Find the Required Table from the Source Code
Table = Bsoup.find("table", { "class" : "wikitable sortable" })
#Count Number of Rows in the table
AllRows = Table.findAll("tr")
for row in AllRows:
#Create a Dictionary to store the Row Details  
  DicRecord = {}
  Columns=row.findAll("td")
  if Columns:    
         DicRecord ['Score'] = Columns [1].text
         Name= Columns [2].find("a")
         DicRecord ['Against'] = Name.text
         DicRecord ['Venue'] = Columns [5].text
         DicRecord ['Date'] =Columns [7].text
         DicRecord ['Result']= Columns [8].text
#Print the Records Founded by the Above step
         print DicRecord  
#Save the records into Scrapperwiki Web site
         scraperwiki.datastore.save(["Score"], DicRecord)                                                                                            import scraperwiki,re
from BeautifulSoup import BeautifulSoup

print "Sachin Tendulkar Oneday Centuries List"
#Get the HTML Page
Gethtml = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_international_cricket_centuries_by_Sachin_Tendulkar')
#Get the Source Code for the Web Page
Bsoup = BeautifulSoup(Gethtml )
#Save the Required Informaiton in the Data Columns with Column names
scraperwiki.metadata.save('data_columns', ['No.','Score', 'Against','Inn.','Test', 'Venue','H/A','Date','Result'])
#Find the Required Table from the Source Code
Table = Bsoup.find("table", { "class" : "wikitable sortable" })
#Count Number of Rows in the table
AllRows = Table.findAll("tr")
for row in AllRows:
#Create a Dictionary to store the Row Details  
  DicRecord = {}
  Columns=row.findAll("td")
  if Columns:    
         DicRecord ['Score'] = Columns [1].text
         Name= Columns [2].find("a")
         DicRecord ['Against'] = Name.text
         DicRecord ['Venue'] = Columns [5].text
         DicRecord ['Date'] =Columns [7].text
         DicRecord ['Result']= Columns [8].text
#Print the Records Founded by the Above step
         print DicRecord  
#Save the records into Scrapperwiki Web site
         scraperwiki.datastore.save(["Score"], DicRecord)