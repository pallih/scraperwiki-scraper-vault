from BeautifulSoup import BeautifulSoup
import urllib
import re
import scraperwiki
 
pageFile = urllib.urlopen("https://registers.cidb.org.za/PublicContractors/ViewContractor?contractorId=993ac544-325d-4d29-bb9f-000121cdf03d")
pageHtml = pageFile.read()
pageFile.close()
 
soup = BeautifulSoup(pageHtml)
search = soup.findAll("div", {"class":"row"})
index = 0
#scraperwiki.sqlite.execute("create table data (main int, data string)")
for base in search:
    label = base.findAll('div', attrs={'class' : 'rowLabel'}, text=True)
    value = base.findAll('div', attrs={'class' : 'rowValue'}, text=True)
    print label
    #print '%d. %s >> %s' % (index, label, value)
    index += 1
    #scraperwiki.sqlite.save(index["Num"], label)
    
    label2 = label
    scraperwiki.sqlite.execute("insert into data values (?,?)", (index, "label2"))  
    scraperwiki.sqlite.commit() 








