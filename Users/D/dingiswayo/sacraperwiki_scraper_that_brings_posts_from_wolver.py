####------------------------------------------------####
####
import scraperwiki
from BeautifulSoup import BeautifulSoup

#passing the url to scraper
ForumHTML= scraperwiki.scrape('http://forums.fertilitycommunity.com/vitro-fertilization-ivf/')

#Creating Data Columns
scraperwiki.metadata.save('Table_Columns',['S.No', 'Title', 'Last Post','Replies', 'Views'])     

#Getting soup 
HTMLSoup=BeautifulSoup(ForumHTML) 

#Retrieving required code
TableBody=HTMLSoup.find("tbody", {"id":"threadbits_forum_169"}) 

#Retrieving table rows
Rows= TableBody.findAll("tr")

#for serial number
count=0

#for each serial number
for row in Rows:
 
    count=count+1  #for each record it will increment number by 1

    NewRecord={}   # Empty record

    tds=row.findAll("td")  #For all table cells

    NewRecord['S.No']=count

    # My required data is not ther in td it slef so i am moving to required filed like below

    # td/div/a/span
    NewRecord['Title']=tds[2].findAll("div")[0].find("a").find("span").string

    # td/div/a 
    NewRecord['Last Post']=tds[3].findAll("div")[0].find("a").string

    #td/a 
    NewRecord['Replies']=tds[4].find("a").string

    #td
    NewRecord['Views']=tds[5].string

    #Saving data to dtabase
    scraperwiki.datastore.save(["S.No"], NewRecord)

print "All Records Saved"



