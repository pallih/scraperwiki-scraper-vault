import scraperwiki 
from BeautifulSoup import BeautifulSoup  


def GetHTML(url):    # generating html
    return scraperwiki.scrape(url)

def GetSoup(HTML):   # generate soup html
    return BeautifulSoup(HTML) 

def Createmetadata():   
      scraperwiki.metadata.save('Column Names',['Country', 'Men', 'Women', 'Mixed', 'Total'])       

def SaveRecords(record):
     scraperwiki.datastore.save(["Country"],record)
     print "Record Saved"

def CreateRecords(Souphtml):
       HTMLTable=Souphtml.findAll("div", {"class":"contentitem"}) #     Table
       table=HTMLTable[1].find("table")
       print table      
       trows=table.findAll("tr") 
       print trows
       count=0
       for tr in trows:
            count=count+1   
            EmptyRecord={}
            tds=tr.findAll("td")
            #print tds
            if tds:
              print len(tds)-1 
              print count
              if count<39:
                if tds[0].text:
                        print tds[0]
                        EmptyRecord["Country"]=tds[0].text
                if tds[4].text:            
                        print tds[4].text
                        EmptyRecord["Men"]=tds[4].text  
                if tds[8].text:
                        print tds[8].text
                        EmptyRecord["Woman"]=tds[8].text
                if tds[12].text:
                        print tds[12].text
                        EmptyRecord["Mixed"]=tds[12].text
                if tds[16].text:
                        print tds[16].text
                        EmptyRecord["Total"]=tds[16].text
                SaveRecords(EmptyRecord)

url='http://results.cwgdelhi2010.org/en/Root.mvc/Medals'
html=GetHTML(url)
print html
soup=GetSoup(html)
print soup
Createmetadata()
CreateRecords(soup)






    





import scraperwiki 
from BeautifulSoup import BeautifulSoup  


def GetHTML(url):    # generating html
    return scraperwiki.scrape(url)

def GetSoup(HTML):   # generate soup html
    return BeautifulSoup(HTML) 

def Createmetadata():   
      scraperwiki.metadata.save('Column Names',['Country', 'Men', 'Women', 'Mixed', 'Total'])       

def SaveRecords(record):
     scraperwiki.datastore.save(["Country"],record)
     print "Record Saved"

def CreateRecords(Souphtml):
       HTMLTable=Souphtml.findAll("div", {"class":"contentitem"}) #     Table
       table=HTMLTable[1].find("table")
       print table      
       trows=table.findAll("tr") 
       print trows
       count=0
       for tr in trows:
            count=count+1   
            EmptyRecord={}
            tds=tr.findAll("td")
            #print tds
            if tds:
              print len(tds)-1 
              print count
              if count<39:
                if tds[0].text:
                        print tds[0]
                        EmptyRecord["Country"]=tds[0].text
                if tds[4].text:            
                        print tds[4].text
                        EmptyRecord["Men"]=tds[4].text  
                if tds[8].text:
                        print tds[8].text
                        EmptyRecord["Woman"]=tds[8].text
                if tds[12].text:
                        print tds[12].text
                        EmptyRecord["Mixed"]=tds[12].text
                if tds[16].text:
                        print tds[16].text
                        EmptyRecord["Total"]=tds[16].text
                SaveRecords(EmptyRecord)

url='http://results.cwgdelhi2010.org/en/Root.mvc/Medals'
html=GetHTML(url)
print html
soup=GetSoup(html)
print soup
Createmetadata()
CreateRecords(soup)






    





