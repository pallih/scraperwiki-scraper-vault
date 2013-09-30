from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

mech = Browser()

#html = scraperwiki.scrape('http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP')

#import lxml.html
#root = lxml.html.fromstring(html)
#trackdata = ['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP', 'Valencia', '2012']
#url = []
url=    [['http://www.motogp.com/en/Results+Statistics/2012/QAT/MotoGP','Losail','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/SPA/MotoGP','Jerez','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/POR/MotoGP','Estoril','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/FRA/MotoGP','Le Mans','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CAT/MotoGP','Catalunya','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GBR/MotoGP','Silverstone','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/NED/MotoGP','Assen','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GER/MotoGP','Sachsenring','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ITA/MotoGP','Mugello','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/USA/MotoGP','Laguna Seca','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/INP/MotoGP','Indianapolis','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CZE/MotoGP','BRNO','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/RSM/MotoGP','Misano','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ARA/MotoGP','Aragon','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/JPN/MotoGP','Motegi','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/MAL/MotoGP','Sepang','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/AUS/MotoGP','Phillip Island','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP','Valencia','2012'],
['http://www.motogp.com/en/Results+Statistics/2011/QAT/MotoGP','Losail','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/SPA/MotoGP','Jerez','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/POR/MotoGP','Estoril','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/FRA/MotoGP','Le Mans','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CAT/MotoGP','Catalunya','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GBR/MotoGP','Silverstone','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/NED/MotoGP','Assen','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ITA/MotoGP','Mugello','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GER/MotoGP','Sachsenring','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/USA/MotoGP','Laguna Seca','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CZE/MotoGP','BRNO','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/INP/MotoGP','Indianapolis','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/RSM/MotoGP','Misano','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ARA/MotoGP','Aragon','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/JPN/MotoGP','Motegi','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/AUS/MotoGP','Phillip Island','2011'],
#['http://www.motogp.com/en/Results+Statistics/2011/MAL/MotoGP','Sepang','2011']]
['http://www.motogp.com/en/Results+Statistics/2011/VAL/MotoGP','Valencia','2011']] 



#track.append('Valencia')
#season.append('2012')


for entry in url:
    print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    
    col = table.tbody(re.compile("t"), recursive=False)
    #print(col[9])
    tds = 0
    count = 0
    nc = 0
    for n in col:
        arr = []
        if col[tds].text == 'Not Classified':
            nc = 1 
            #print (nc)
        #if nc == 1:
            #print('i am 1')
        if (count==10 or tds == 0) and nc == 0:
            #if (col[tds].string == None):
                #tds+=1
            #print(col[3])
            temp = col[3].text
            firstname = temp.split()
            print(firstname[1])

#lastname = re.search('(.*)[^ Km/h]',tds[3].text).group(0)

            arr = [entry[1],entry[2],col[tds].text,col[tds+1].text,col[tds+2].text,col[tds+3].text,col[tds+4].text,col[tds+5].string,col[tds+6].string,col[tds+7].string,col[tds+8].string]
            #print(col[tds+3])
            count = 0 
    
        if len(n) > 1:
            #print(n)
            #print(n('td'))
            a = n('td')
    
            if nc == 1:
                #print ('nc == 1')
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].string]
            else:
                #print ('nc == 0')
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].string]    
            
            #print(a[0].string,a[1].string,a[2].string,a[3].text,a[4].string,a[5].string,a[6].string,a[7].string,a[8].string)
            #print (a[3].text)
        
        if not arr == []:
            scraperwiki.sqlite.save(unique_keys=["circuit", "season", "rider"], data={"circuit":arr[0], "season":arr[1], "pos":arr[2],"points":arr[3], "number":arr[4],"rider":arr[5],"nation":arr[6],"team":arr[7],"bike":arr[8],"speed":arr[9],"timegap":arr[10]})
        tds += 1
        count+=1







#resContainer =  soup.find("div", { "id" : "midmain_result"})
#rownumber = 0

#table = soup.find("table")

#print (table.tbody('tr'))
#col = table.tbody("tr",attrs={'class': None})
#col = table.tbody(re.compile("t"), recursive=False)

#maxRuns = len(col)/9
#o = [col[0]


#print (len(col)/9)
#print (col.getshape())
#print(col)









from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

mech = Browser()

#html = scraperwiki.scrape('http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP')

#import lxml.html
#root = lxml.html.fromstring(html)
#trackdata = ['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP', 'Valencia', '2012']
#url = []
url=    [['http://www.motogp.com/en/Results+Statistics/2012/QAT/MotoGP','Losail','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/SPA/MotoGP','Jerez','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/POR/MotoGP','Estoril','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/FRA/MotoGP','Le Mans','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CAT/MotoGP','Catalunya','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GBR/MotoGP','Silverstone','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/NED/MotoGP','Assen','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GER/MotoGP','Sachsenring','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ITA/MotoGP','Mugello','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/USA/MotoGP','Laguna Seca','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/INP/MotoGP','Indianapolis','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CZE/MotoGP','BRNO','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/RSM/MotoGP','Misano','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ARA/MotoGP','Aragon','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/JPN/MotoGP','Motegi','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/MAL/MotoGP','Sepang','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/AUS/MotoGP','Phillip Island','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP','Valencia','2012'],
['http://www.motogp.com/en/Results+Statistics/2011/QAT/MotoGP','Losail','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/SPA/MotoGP','Jerez','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/POR/MotoGP','Estoril','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/FRA/MotoGP','Le Mans','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CAT/MotoGP','Catalunya','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GBR/MotoGP','Silverstone','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/NED/MotoGP','Assen','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ITA/MotoGP','Mugello','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GER/MotoGP','Sachsenring','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/USA/MotoGP','Laguna Seca','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CZE/MotoGP','BRNO','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/INP/MotoGP','Indianapolis','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/RSM/MotoGP','Misano','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ARA/MotoGP','Aragon','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/JPN/MotoGP','Motegi','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/AUS/MotoGP','Phillip Island','2011'],
#['http://www.motogp.com/en/Results+Statistics/2011/MAL/MotoGP','Sepang','2011']]
['http://www.motogp.com/en/Results+Statistics/2011/VAL/MotoGP','Valencia','2011']] 



#track.append('Valencia')
#season.append('2012')


for entry in url:
    print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    
    col = table.tbody(re.compile("t"), recursive=False)
    #print(col[9])
    tds = 0
    count = 0
    nc = 0
    for n in col:
        arr = []
        if col[tds].text == 'Not Classified':
            nc = 1 
            #print (nc)
        #if nc == 1:
            #print('i am 1')
        if (count==10 or tds == 0) and nc == 0:
            #if (col[tds].string == None):
                #tds+=1
            #print(col[3])
            temp = col[3].text
            firstname = temp.split()
            print(firstname[1])

#lastname = re.search('(.*)[^ Km/h]',tds[3].text).group(0)

            arr = [entry[1],entry[2],col[tds].text,col[tds+1].text,col[tds+2].text,col[tds+3].text,col[tds+4].text,col[tds+5].string,col[tds+6].string,col[tds+7].string,col[tds+8].string]
            #print(col[tds+3])
            count = 0 
    
        if len(n) > 1:
            #print(n)
            #print(n('td'))
            a = n('td')
    
            if nc == 1:
                #print ('nc == 1')
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].string]
            else:
                #print ('nc == 0')
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].string]    
            
            #print(a[0].string,a[1].string,a[2].string,a[3].text,a[4].string,a[5].string,a[6].string,a[7].string,a[8].string)
            #print (a[3].text)
        
        if not arr == []:
            scraperwiki.sqlite.save(unique_keys=["circuit", "season", "rider"], data={"circuit":arr[0], "season":arr[1], "pos":arr[2],"points":arr[3], "number":arr[4],"rider":arr[5],"nation":arr[6],"team":arr[7],"bike":arr[8],"speed":arr[9],"timegap":arr[10]})
        tds += 1
        count+=1







#resContainer =  soup.find("div", { "id" : "midmain_result"})
#rownumber = 0

#table = soup.find("table")

#print (table.tbody('tr'))
#col = table.tbody("tr",attrs={'class': None})
#col = table.tbody(re.compile("t"), recursive=False)

#maxRuns = len(col)/9
#o = [col[0]


#print (len(col)/9)
#print (col.getshape())
#print(col)









