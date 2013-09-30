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
url=    [['http://www.motogp.com/en/Results+Statistics/2012/QAT/MotoGP/QP','Losail','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/SPA/MotoGP/QP','Jerez','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/POR/MotoGP/QP','Estoril','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/FRA/MotoGP/QP','Le Mans','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CAT/MotoGP/QP','Catalunya','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GBR/MotoGP/QP','Silverstone','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/NED/MotoGP/QP','Assen','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GER/MotoGP/QP','Sachsenring','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ITA/MotoGP/QP','Mugello','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/USA/MotoGP/QP','Laguna Seca','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/INP/MotoGP/QP','Indianapolis','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CZE/MotoGP/QP','BRNO','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/RSM/MotoGP/QP','Misano','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ARA/MotoGP/QP','Aragon','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/JPN/MotoGP/QP','Motegi','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/MAL/MotoGP/QP','Sepang','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/AUS/MotoGP/QP','Phillip Island','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP/QP','Valencia','2012'],
['http://www.motogp.com/en/Results+Statistics/2011/QAT/MotoGP/QP','Losail','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/SPA/MotoGP/QP','Jerez','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/POR/MotoGP/QP','Estoril','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/FRA/MotoGP/QP','Le Mans','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CAT/MotoGP/QP','Catalunya','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GBR/MotoGP/QP','Silverstone','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/NED/MotoGP/QP','Assen','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ITA/MotoGP/QP','Mugello','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GER/MotoGP/QP','Sachsenring','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/USA/MotoGP/QP','Laguna Seca','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CZE/MotoGP/QP','BRNO','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/INP/MotoGP/QP','Indianapolis','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/RSM/MotoGP/QP','Misano','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ARA/MotoGP/QP','Aragon','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/JPN/MotoGP/QP','Motegi','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/AUS/MotoGP/QP','Phillip Island','2011'],
#['http://www.motogp.com/en/Results+Statistics/2011/MAL/MotoGP','Sepang','2011']]
['http://www.motogp.com/en/Results+Statistics/2011/VAL/MotoGP/QP','Valencia','2011']] 



#track.append('Valencia')
#season.append('2012')


for entry in url:
    print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    
    col = table.tbody(re.compile("t"), recursive=False)
    tds = 0
    count = 0
    nc = 0
    for n in col:
        arr = []
        if col[tds].text == 'Not Classified':
            nc = 1 
        if (count==10 or tds == 0) and nc == 0:

            arr = [entry[1],entry[2],col[tds].text,col[tds+1].text,col[tds+2].text,col[tds+3].text,col[tds+4].text,col[tds+5].string,col[tds+6].string,col[tds+7].string,col[tds+8].text]
            count = 0 
    
        if len(n) > 1:

            a = n('td')
    
            if nc == 1:
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].text]
            else:
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].text]    
        
        if not arr == []:
            print(arr)

            scraperwiki.sqlite.save(unique_keys=["circuit", "season", "rider"],data={"circuit":arr[0], "season":arr[1], "pos":arr[2],"number":arr[3],"rider":arr[4],"nation":arr[5],"team":arr[6],"bike":arr[7],"speed":arr[8],"time":arr[9],"gap":arr[10]})
        tds += 1
        count+=1







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
url=    [['http://www.motogp.com/en/Results+Statistics/2012/QAT/MotoGP/QP','Losail','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/SPA/MotoGP/QP','Jerez','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/POR/MotoGP/QP','Estoril','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/FRA/MotoGP/QP','Le Mans','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CAT/MotoGP/QP','Catalunya','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GBR/MotoGP/QP','Silverstone','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/NED/MotoGP/QP','Assen','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/GER/MotoGP/QP','Sachsenring','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ITA/MotoGP/QP','Mugello','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/USA/MotoGP/QP','Laguna Seca','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/INP/MotoGP/QP','Indianapolis','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/CZE/MotoGP/QP','BRNO','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/RSM/MotoGP/QP','Misano','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/ARA/MotoGP/QP','Aragon','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/JPN/MotoGP/QP','Motegi','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/MAL/MotoGP/QP','Sepang','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/AUS/MotoGP/QP','Phillip Island','2012'],
['http://www.motogp.com/en/Results+Statistics/2012/VAL/MotoGP/QP','Valencia','2012'],
['http://www.motogp.com/en/Results+Statistics/2011/QAT/MotoGP/QP','Losail','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/SPA/MotoGP/QP','Jerez','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/POR/MotoGP/QP','Estoril','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/FRA/MotoGP/QP','Le Mans','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CAT/MotoGP/QP','Catalunya','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GBR/MotoGP/QP','Silverstone','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/NED/MotoGP/QP','Assen','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ITA/MotoGP/QP','Mugello','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/GER/MotoGP/QP','Sachsenring','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/USA/MotoGP/QP','Laguna Seca','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/CZE/MotoGP/QP','BRNO','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/INP/MotoGP/QP','Indianapolis','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/RSM/MotoGP/QP','Misano','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/ARA/MotoGP/QP','Aragon','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/JPN/MotoGP/QP','Motegi','2011'],
['http://www.motogp.com/en/Results+Statistics/2011/AUS/MotoGP/QP','Phillip Island','2011'],
#['http://www.motogp.com/en/Results+Statistics/2011/MAL/MotoGP','Sepang','2011']]
['http://www.motogp.com/en/Results+Statistics/2011/VAL/MotoGP/QP','Valencia','2011']] 



#track.append('Valencia')
#season.append('2012')


for entry in url:
    print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table")
    
    col = table.tbody(re.compile("t"), recursive=False)
    tds = 0
    count = 0
    nc = 0
    for n in col:
        arr = []
        if col[tds].text == 'Not Classified':
            nc = 1 
        if (count==10 or tds == 0) and nc == 0:

            arr = [entry[1],entry[2],col[tds].text,col[tds+1].text,col[tds+2].text,col[tds+3].text,col[tds+4].text,col[tds+5].string,col[tds+6].string,col[tds+7].string,col[tds+8].text]
            count = 0 
    
        if len(n) > 1:

            a = n('td')
    
            if nc == 1:
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].text]
            else:
                arr = [entry[1],entry[2],a[0].text,a[1].text,a[2].text,a[3].text,a[4].text,a[5].string,a[6].string,a[7].string,a[8].text]    
        
        if not arr == []:
            print(arr)

            scraperwiki.sqlite.save(unique_keys=["circuit", "season", "rider"],data={"circuit":arr[0], "season":arr[1], "pos":arr[2],"number":arr[3],"rider":arr[4],"nation":arr[5],"team":arr[6],"bike":arr[7],"speed":arr[8],"time":arr[9],"gap":arr[10]})
        tds += 1
        count+=1







