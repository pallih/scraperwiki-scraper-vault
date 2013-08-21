#/usr/bin/env python# -*- coding: latin-1 -*-

from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import gc
import scraperwiki
from scraperwiki import sqlite
import re
import numpy
mech = Browser()
posDict = dict()
nameDict = dict();
#name possibilities in the CSV files
nameDict['Pos.'] = 'pos'
nameDict['Num.'] = 'num'
nameDict['Rider'] = 'rider'
nameDict['Nation'] = 'nation'
nameDict['Km/h'] = 'speed'
nameDict['Time'] = 'totaltime'
nameDict['Gap1st/Prev.'] = 'timegap'
nameDict['Points'] = 'points'
nameDict['Time/Gap'] = 'timegap'
nameDict['Bike'] = 'bike'
nameDict['Team'] = 'team'

weatherExch = []
sessionExch = []
polesExch = []


#scraperwiki::sqliteexecute('create table sessionResults'); 
#scraperwiki.sqlite.execute('create table sessionResults')

def saveWeatherConditions(url, trackname, season, session):
    tn = 'weatherConditions'

    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    try:
        table = soup.find("div",{"id" : "main_result"})
        col = table.findAll("span")    
        for span in col:
            if (span.text.find('Track Condition:') > -1):
                condition = re.search('(?<=Track Condition: )(.*)',span.text).group(0)
                #print (condition)
            if (span.text.find('Air: ') > -1):
                airTemp = re.search('(?<=Air: )([0-9][0-9]*)',span.text).group(0)
                #print (airTemp) 
            if (span.text.find('Humidity: ') > -1):
                humidity = re.search('(?<=Humidity: )([0-9][0-9]*)',span.text).group(0)
                #print (humidity)  
            if (span.text.find('Ground: ') > -1):
                groundTemp = re.search('(?<=Ground: )([0-9][0-9]*)',span.text).group(0)
                #print (groundTemp) 

    
        #print('   Weatherconditions: '+trackname+' , '+session+', '+season+', '+condition+', '+airTemp+', '+humidity+', '+groundTemp)
        #scraperwiki.sqlite.save(unique_keys=["circuit", "season", "session"], table_name=tn, data={"circuit":trackname, "season":season, "session":session, "condition":condition,"airTemp":airTemp,"humidity":humidity,"groundTemp":groundTemp }, verbose = 0)  
        wData={"circuit":trackname, "season":season, "session":session, "condition":condition,"airTemp":airTemp,"humidity":humidity,"groundTemp":groundTemp }
        print (wData)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season", "session"], table_name="weatherConditions", data=wData, verbose = 1)
    except Exception,e: 
            print ('!!! Could not save weather conditions for '+trackname+' season: '+season+' with error: '+str(e))


def savePolepositions(url, trackname, season):
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
### Save pole positions
    try:
        tn = 'polePositions'

        table = soup.find("table",{"class" : "width100 marginbot10"})
        col = table.find("tr")
        tds=col("td")
        rider = tds[1].text
        time = tds[2].text
        speed = re.search('([0-9][0-9]*)',tds[3].text).group(0)
        print('   Polepsoitions: '+trackname+', '+season+', '+rider+', '+time+', '+speed)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season"], table_name=tn, data={"circuit":trackname, "season":season, "rider":rider, "time":time,"speed":speed}, verbose = 0) 
    except Exception,e: 
        print ('!!! Could not save pole position for '+trackname+' season: '+season+' with error: '+str(e))
### Save fastest laps
    try:
        tn = 'fastestLap'
    
        table = soup.find("table",{"class" : "width100 marginbot10"})
        col = table.findAll("tr")
        tds=col[1]("td")
        lap = re.search('[^Lap: ](.*)',tds[0].text).group(0)
    
        rider = tds[1].text
        time = tds[2].text
        speed = re.search('(.*)[^ Km/h]',tds[3].text).group(0)
        #print(lap)
        print('   fastest lap: '+trackname+', '+season+', '+rider+', '+lap+', '+time+', '+speed)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season"], table_name=tn, data={"circuit":trackname, "season":season,"lap":lap, "rider":rider, "time":time,"speed":speed}, verbose = 0)
    except Exception,e: 
        print ('!!! Could not save fastest lap for '+trackname+' season: '+season+' with error: '+str(e))
### Save circuit records  
    try:  
        tn = 'circuitRecord'
        table = soup.find("table",{"class" : "width100 marginbot10"})
        col = table.findAll("tr")
        tds=col[2]("td")
        date = tds[0].text
    
        rider = tds[1].text
        time = tds[2].text
        speed = re.search('(.*)[^ Km/h]',tds[3].text).group(0)
        #print(lap)
        print('   Circuit Records: '+trackname+', '+season +', '+rider+', '+date+', '+time+', '+speed)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season"], table_name=tn, data={"circuit":trackname, "season":season,"date":date, "rider":rider, "time":time,"speed":speed}, verbose = 0)

    except Exception,e: 
        print ('!!! Could not save circuit record for '+trackname+' season: '+season+' with error: '+str(e))
    try:
        tn = 'bestLaps'
        table = soup.find("table",{"class" : "width100 marginbot10"})
        col = table.findAll("tr")
        tds=col[3]("td")
        #track = entry[1]
        #season =  entry[2]
        date = tds[0].text
    
        rider = tds[1].text
        time = tds[2].text
        speed = re.search('(.*)[^ Km/h]',tds[3].text).group(0)
        #print(lap)
        #print(track,season,rider,date,time,speed)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season"], table_name=tn, data={"circuit":trackname, "season":season,"date":date, "rider":rider, "time":time,"speed":speed})
    except Exception,e: 
            print ('!!! Could not save bestlaps for '+trackname+' season: '+season+' with error: '+str(e))


def saveQ1Data(url, trackname, season, session, gpname):
    try:  
        bigdata=[]
        tn = 'sessionResults'
        session = str(session)
        page = mech.open(url)
        html = page.read()
        soup = BeautifulSoup(html)
        table = soup.find("table")
        
        print('session: '+session+' in '+gpname)
        colHeader = table.thead.findAll('th')
        headerCounter = 0
        posDict = {}
        dictArr = []
        default = -1
        for entr in colHeader:
            #print(entr.text)
            try:
                #print (entr.text)
                posDict[str(nameDict[entr.text])] = headerCounter 
                dictArr.append(str(nameDict[entr.text]))
                #if (row[0] == 'TimeAST'):
                #timeForm = str(col[0])
                #print(timeForm)
                headerCounter +=1
            except:
                headerCounter +=1
                #print('err')
        #print('header total: '+str(headerCounter))
        #print(posDict)
        print(dictArr)
    
    #def roll(): 
        #print(table.tbody)
        
        cells = table.tbody.findAll('td')
        cellCounter = 0
        runs = 0
        data = {}
        notClassified = 'false';
        #print(cells)
        print('------------- new run -----------')
        for cell in cells:
            if (cell.text not in ('Not Classified','Not Finished 1st Lap',"Not Starting" ,"Excluded")):
            #print(str(dictArr[cellCounter])+' = '+str(cell.text)+' in cellCounter '+str(cellCounter))
                if (dictArr[cellCounter] == 'timegap' and str(cell.text) == ''):
                    print('***** ***** ***** ***** ***** ***** ***** ***** ***** ')
                    print ('NO TIMEGAP FOUND! I SHOULD SET TOTALTIME: '+str(data['totaltime'])) 
                    print(cell.text)
                    print('***** ***** ***** ***** ***** ***** ***** ***** ***** ')
                    data[dictArr[cellCounter]] = data['totaltime']
                    cellCounter+=1

                else:
                    data[dictArr[cellCounter]] = cell.text
                    cellCounter+=1
            else:
                notClassified = 'true';
            if cellCounter == headerCounter:
                #print('-------------')
                cellCounter = 0
                data['gpname'] = gpname
                data['circuit'] = trackname
                data['season'] = season
                data['session'] = session
                #print(data)
                runs+=1
                if (str(data['pos']) is ''):
                    data['pos'] = runs
                if (notClassified == 'true'):
                    data['dnf'] = 'true'
                #print(data)
                #print('runs: '+str(runs)+' is the same as pos? '+data['pos'])
                bigdata.append(data.copy())
                data = {}
                if len(bigdata)>1000:
                    storeSessionData(bigdata)
                    bigdata=[]
                
                
        storeSessionData(bigdata)
        bigdata=[]
    except Exception,e:
        print("Error: "+str(e))

def storeSessionData(input):
    try:
        print(input)
        scraperwiki.sqlite.save(unique_keys=["circuit", "season", "rider", "session"], table_name='sessionResults', data=input,verbose=0)
    except Exception,e:
        print('*******************************************************************')
        print("*** Error storing data: "+str(e))
        print('*******************************************************************')


def runWeatherArr(input):
    #chunkHolder = []
    for nd in input:
        saveWeatherConditions(nd[0], nd[1], nd[2], nd[3])
    #weatherExch = []

def runSessionArr(input):
    for nd in input:
        saveQ1Data(nd[0], nd[1], nd[2], nd[3], nd[4])
    #sessionExch = []

def runPolesArr(input):
    for nd in input:
        savePolepositions(nd[0], nd[1], nd[2])
    #polesExch = []


url= 'http://www.motogp.com/en/Results+Statistics/'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)
### Gather URL's for 500cc and MotoGP class ###
motoGPurlArray = []
yearsObject =  sorted(soup.find("div", { "id" : "advanced_search"}).findAll("div")[16].find("label").findAll("option"), reverse=True)
yearsArray = []

def runYears(RunYear, raceNum):
    print('Running year '+str(RunYear))
    for year in yearsObject :
        if (int(year.text) == int(RunYear)):
            url= 'http://www.motogp.com/en/Results+Statistics/'+year.text
            page = mech.open(url)
            html = page.read()
            soup = BeautifulSoup(html)
            racesObject =  soup.find("select", { "id" : "event"}).findAll("option")
            racesArray = []
            print(racesObject)
            for race in racesObject[(raceNum-1):raceNum]:
                try:
                    print(year.text+': '+race.attrs[1][1].split(' - ')[0])
                    #print(race.attrs[0][1])
                    url= 'http://www.motogp.com/en/Results+Statistics/'+year.text+'/'+race.attrs[0][1]
                    page = mech.open(url)
                    html = page.read()
                    soup = BeautifulSoup(html)
                    classesObject =  soup.find("select", { "id" : "category"}).findAll("option")
                    classesArray = []
                    for RaceClass in classesObject : 
                        try:                
                            if (RaceClass.attrs[0][1] == 'MotoGP') or (RaceClass.attrs[0][1] == '500cc'): 
                                url= 'http://www.motogp.com/en/Results+Statistics/'+year.text+'/'+race.attrs[0][1]+'/'+RaceClass.attrs[0][1]
                                #print('raceclass: '+url)  
                                ## Save weather conditions
                                page = mech.open(url)
                                html = page.read()
                                soup = BeautifulSoup(html)
                                sessionsObject =  soup.find("select", { "id" : "session"}).findAll("option")
                                #print ('sessionsObject :'+sessionsObject.string)
                                sessionsArray = []
                                for session in sessionsObject :
                                        sessionval = session.attrs[0][1]
                                        suburl = url+'/'+sessionval
                                        #if (sessionval.find('RAC') > -1):
                                        #saveQ1Data(suburl, race.text.split(' - ')[1], year.text, sessionval, race.attrs[1][1].split(' - ')[0])
                                        global sessionExch
                                        sessionExch.append([suburl, race.text.split(' - ')[1], year.text, sessionval, race.attrs[1][1].split(' - ')[0]])
                                        ## save WeatherConditions
                                        if (int(year.text) >= 2005):
                                            ## save WeatherConditions
                                            #saveWeatherConditions(suburl, race.text.split(' - ')[1], year.text,sessionval)
                                            global weatherExch
                                            weatherExch.append([suburl, race.text.split(' - ')[1], year.text,sessionval])
                                ## save polepositions
                                #savePolepositions(url, race.text.split(' - ')[1], year.text)
                                global polesExch
                                polesExch.append([url, race.text.split(' - ')[1], year.text])
                        except Exception,e: 
                            print ('!!! Could not sub-run2 for '+url+' with error: '+str(e))
        
        
                except Exception,e: 
                    print ('!!! Could not run for '+url+' with error: '+str(e))
        gc.collect()
    print('***** finished collecting data ******')
    gc.collect()
    runSessionArr(sessionExch)
    sessionExch = []
    print('***** finished saving session data ******')
    
    if (bool(weatherExch)):
        print(weatherExch)
        gc.collect()
        runWeatherArr(weatherExch)
        weatherExch = []
    print('***** finished saving weather data ******')
    gc.collect()
    runPolesArr(polesExch)
    polesExch = []
    print('***** finished saving poles data ******')

for y in ['2013']:#, '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996','1995','1994','1993','1992','1991','1990', '1989', '1988', '1988','1987','1986','1985','1984','1983','1982','1981','1980','1979','1978','1977','1976','1975','1974','1973','1972','1971','1970','1969','1968','1967','1966','1965','1964','1963','1962','1961','1960','1959','1958','1957','1956','1955','1954','1953','1952','1951','1950','1949','1948']:
    runYears(y, 10)
    #procesWeather(y)

#1. Commercial Bank Grand Prix of Qatar - Losail Circuit
#2. Red Bull Grand Prix of The Americas - Circuit Of The Americas
#3. Gran Premio bwin de Espa�a - Jerez Circuit
#4. Monster Energy Grand Prix de France - Le Mans Circuit
#5. Gran Premio d'Italia TIM - Mugello Circuit
#6. Gran Premi Aperol de Catalunya - Catalunya Circuit
#7. Iveco TT Assen - TT Circuit Assen
#8. eni Motorrad Grand Prix Deutschland - Sachsenring Circuit
#9. Red Bull U.S. Grand Prix - Mazda Raceway Laguna Seca
#10. Red Bull Indianapolis Grand Prix - Indianapolis Motor Speedway
#11. bwin Grand Prix Cesk� republiky - Brno Circuit
#12. Hertz British Grand Prix - Silverstone Circuit
#13. GP Aperol di San Marino e della Riviera di Rimini - Misano World Circuit
#14. Gran Premio Iveco de Arag�n - MotorLand Aragon
#15. Malaysian Motorcycle Grand Prix - Sepang Circuit
#16. Australian Grand Prix - Phillip Island Circuit
#17. Grand Prix of Japan - Motegi Circuit
#18. Gran Premio Generali de la Comunitat Valenciana - Comunitat Valenciana

print('***** ***** ***** ***** ***** ***** ***** ***** ***** ')
print('***** ***** ***** *!! All DONE !!** ***** ***** ***** ')
print('***** ***** ***** ***** ***** ***** ***** ***** ***** ')

#MOTOGP 
