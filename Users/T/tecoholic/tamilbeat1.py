###############################################################################
# MP3 ID3 tag data collector to extract data from Tamilbeat.com
###############################################################################

import scraperwiki
import string
from BeautifulSoup import BeautifulSoup

#scrapes the webpage urls for individual films
def addpages(newsoup,id):
    table = newsoup.find('table',{"id":"AutoNumber4"})
    atags = table.findAll('a')    
    # Now creating dataset for saving
    #creating record for saving  
    for a in atags:                      
        valid = 1
        tempurl=a['href'].strip('index.html')
        #this loop is  detect the duplicates by comparing with the overall list "links"
        for i in range(len(links)):
            if links[i]==tempurl:
                valid=0   #Validity is set as 0 when a dupliacte is detected
                break
            else:
                pass
        #the data is added to the datastore only if it is not a duplicate
        if valid==1:
            links.append(tempurl)
            record['id']=id
            id=id+1
            record['Film']=a.text.strip('&nbsp;')
            record['Url']='http://www.tamilat.com/tamilsongs'+tempurl.strip('..')
            scraperwiki.sqlite.save(['id'],record)
    return id

#Links to the pages that contain the film listing
listing=['http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/index.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/1-1.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/b-d.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/e-h.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/i-j.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/k-l.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/m-m.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/n-o.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/p-p.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/r-s.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/t-t.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/u-z.html']

links=[]   #To store the links as a list.This helps to remove duplicates by comparison
record={}  #To create a record to be added to the data store
nid=1      #This acts as the counter to count the number of links collected in the pages

for link in listing:
    print link
    url2=link
    html2 = scraperwiki.scrape(url2)
    soup2 = BeautifulSoup(html2)
    nid=addpages(soup2,nid)
    print nid
###############################################################################
# MP3 ID3 tag data collector to extract data from Tamilbeat.com
###############################################################################

import scraperwiki
import string
from BeautifulSoup import BeautifulSoup

#scrapes the webpage urls for individual films
def addpages(newsoup,id):
    table = newsoup.find('table',{"id":"AutoNumber4"})
    atags = table.findAll('a')    
    # Now creating dataset for saving
    #creating record for saving  
    for a in atags:                      
        valid = 1
        tempurl=a['href'].strip('index.html')
        #this loop is  detect the duplicates by comparing with the overall list "links"
        for i in range(len(links)):
            if links[i]==tempurl:
                valid=0   #Validity is set as 0 when a dupliacte is detected
                break
            else:
                pass
        #the data is added to the datastore only if it is not a duplicate
        if valid==1:
            links.append(tempurl)
            record['id']=id
            id=id+1
            record['Film']=a.text.strip('&nbsp;')
            record['Url']='http://www.tamilat.com/tamilsongs'+tempurl.strip('..')
            scraperwiki.sqlite.save(['id'],record)
    return id

#Links to the pages that contain the film listing
listing=['http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/index.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/1-1.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/b-d.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/e-h.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/i-j.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/k-l.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/m-m.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/n-o.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/p-p.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/r-s.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/t-t.html','http://www.tamilat.com/tamilsongs/movies%20a%20to%20z/u-z.html']

links=[]   #To store the links as a list.This helps to remove duplicates by comparison
record={}  #To create a record to be added to the data store
nid=1      #This acts as the counter to count the number of links collected in the pages

for link in listing:
    print link
    url2=link
    html2 = scraperwiki.scrape(url2)
    soup2 = BeautifulSoup(html2)
    nid=addpages(soup2,nid)
    print nid
