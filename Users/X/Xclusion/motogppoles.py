from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

mech = Browser()

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


for entry in url:
    #print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table",{"class" : "width100 marginbot10"})
    col = table.find("tr")
    tds=col("td")
    track = entry[1]
    season =  entry[2]
    rider = tds[1].text
    time = tds[2].text
    speed = re.search('([0-9][0-9]*)',tds[3].text).group(0)

    print(track,season,rider,time,speed)
    scraperwiki.sqlite.save(unique_keys=["circuit", "season"], data={"circuit":track, "season":season, "rider":rider, "time":time,"speed":speed})



from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

mech = Browser()

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


for entry in url:
    #print (entry[1])
    page = mech.open(entry[0])
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table",{"class" : "width100 marginbot10"})
    col = table.find("tr")
    tds=col("td")
    track = entry[1]
    season =  entry[2]
    rider = tds[1].text
    time = tds[2].text
    speed = re.search('([0-9][0-9]*)',tds[3].text).group(0)

    print(track,season,rider,time,speed)
    scraperwiki.sqlite.save(unique_keys=["circuit", "season"], data={"circuit":track, "season":season, "rider":rider, "time":time,"speed":speed})



