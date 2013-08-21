#!/usr/bin/env python
# -*- coding: latin-1 -*-
import lxml.html, urllib,csv,scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import datetime
import numpy 
import csv   
import time
import re

# tracks and their selected weatherstation
trackURLDict = dict()
trackURLDict['A1-Ring'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IBAYERNM4&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Albert Park'] = 'http://dutch.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IVICMELB2&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Imola'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IBOLOGNA10&month=!MONTH*&day=!DAY*&year=!YEAR*'
trackURLDict['Monza'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IMILANOR3&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Interlagos'] = 'http://www.wunderground.com/history/airport/SBSP/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Sakhir'] = 'http://www.wunderground.com/history/airport/OBBI/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Buddh International Circuit'] = 'http://www.wunderground.com/history/airport/VIDP/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Circuit de Catalunya'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=MD2727&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Monte Carlo'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IBEAUSOL1&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Magny-Cours'] = 'http://www.wunderground.com/history/airport/LFOA/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Montreal'] = 'http://www.wunderground.com/history/airport/CYHU/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Circuit of the Americas'] = 'http://www.wunderground.com/history/airport/KAUS/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Silverstone'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=INORTHAM5&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Fuji Speedway'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=ISHIZUOK2&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Hockenheim'] = 'http://www.wunderground.com/history/station/10729/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Hungaroring'] = 'http://www.wunderground.com/history/airport/LHBP/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Indianapolis'] = 'http://www.wunderground.com/history/airport/KEYE/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Istanbul Park'] = 'http://www.wunderground.com/history/airport/LTBA/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Korean International Circuit'] = 'http://www.wunderground.com/history/airport/RKJB/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Singapore'] = 'http://www.wunderground.com/history/airport/WSSS/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Nurburgring'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=MAP998&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Sepang'] = 'http://www.wunderground.com/history/airport/WMKK/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Shanghai'] = 'http://www.wunderground.com/history/airport/ZSSS/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Spa-Francorchamps'] = 'http://www.wunderground.com/history/station/06490/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Suzuka'] = 'http://www.wunderground.com/history/airport/RJGG/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'
trackURLDict['Valencia Street Circuit'] = 'http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=IVALENCI15&day=!DAY*&month=!MONTH*&year=!YEAR*'
trackURLDict['Abu Dhabi'] = 'http://www.wunderground.com/history/airport/OMAA/!YEAR*/!MONTH*/!DAY*/DailyHistory.html'

csvDict = dict();
nameDict = dict();
#name possibilities in the CSV files / translations for database colums
nameDict['Wind SpeedKm/h'] = 'windspeed'
nameDict['WindSpeedKMH'] = 'windspeed'
nameDict['Sea Level PressurehPa'] = 'pressure'
nameDict['PressurehPa'] = 'pressure'
nameDict['Precipitationmm'] = 'precipitation'
nameDict['HourlyPrecipMM'] = 'precipitation'
nameDict['Humidity'] = 'humidity'
nameDict['TemperatureC'] = 'temperature'
nameDict['Conditions'] = 'conditions'
nameDict['TimeAST'] = 'time'
nameDict['Time'] = 'time'

tracknameDict = {'A1-Ring':'A1-Ring' ,'Albert Park':'Albert Park' ,'Imola':'Imola' ,'Monza':'Monza' ,'Interlagos':'Interlagos' ,'Sakhir':'Bahrain' ,'Buddh International Circuit':'Buddh International Circuit' ,'Circuit de Catalunya':'Circuit de Catalunya' ,'Monte Carlo':'Monaco' ,'Magny-Cours':'Magny-Cours' ,'Montreal':'Circuit Gilles Villeneuve' ,'Circuit of the Americas':'Circuit of the Americas' ,'Silverstone':'Silverstone' ,'Fuji Speedway':'Fuji Speedway' ,'Hockenheim':'Hockenheim' ,'Hungaroring':'Hungaroring' ,'Indianapolis':'Indianapolis' ,'Istanbul Park':'Istanbul Park' ,'Korean International Circuit':'Yeongam' ,'Singapore':'Marina Bay Street Circuit' ,'Nurburgring':'Nurburgring',u'N\xfcrburgring':'Nurburgring' ,'Sepang':'Sepang' ,'Shanghai':'Shanghai' ,'Spa-Francorchamps':'Spa-Francorchamps' ,'Suzuka':'Suzuka' ,'Valencia Street Circuit':'Valencia Street Circuit' ,'Abu Dhabi':'Yas Marina'}


#def procesRow(row,circuit, dateStr):
def procesRow(bigList,circuit, dateStr):
    #print('Entered procesRow with:')
    #print(bigList)
    length = len(bigList)
    temp = 0
    precipitation = 0
    humidity = 0
    pressure = 0
    windspeed = 0
    condition = ''
    for obj in bigList[0]:
        #print(obj)
        #print(obj[csvDict['temperature']])
        #print(obj[csvDict['precipitation']])
        #print(obj[csvDict['humidity']])
        #print(obj[csvDict['pressure']])
        #print(obj[csvDict['windspeed']])
        if (obj[csvDict['temperature']]!='' and obj[csvDict['temperature']] not in ('N/A', '-')):temp+=float(obj[csvDict['temperature']])
        if (obj[csvDict['precipitation']]!='' and obj[csvDict['precipitation']] not in ('N/A', '-')):precipitation +=float(obj[csvDict['precipitation']])
        if (obj[csvDict['humidity']]!='' and obj[csvDict['humidity']] not in ('N/A', '-')):humidity +=float(obj[csvDict['humidity']])
        if (obj[csvDict['windspeed']]!='' and obj[csvDict['windspeed']] not in ('N/A', '-')):pressure+=float(obj[csvDict['pressure']])
        if (obj[csvDict['windspeed']]!='' and obj[csvDict['windspeed']] not in ('N/A', '-')):windspeed +=float(obj[csvDict['windspeed']])
        if (obj[csvDict['conditions']] != ''):
            condition = obj[csvDict['conditions']]
    temp = (temp/length)
    #precipitation = (precipitation /length)
    humidity = (humidity /length)
    pressure = (pressure /length)
    windspeed = (windspeed /length)
    season = dateStr.split('-')[0]
    scraperwiki.sqlite.save(unique_keys=["circuit", "date"], table_name='weatherHistory', data={"circuit":tracknameDict[circuit], "date":dateStr, 'season':season, "windspeed":windspeed , 'pressure':pressure ,'precipitation':precipitation ,'humidity':humidity,'temperature':temp,'conditions':condition })
    #scraperwiki.sqlite.save(unique_keys=["circuit", "date"], table_name='weatherHistory', data={"circuit":circuit, "date":dateStr, "windspeed":row[csvDict['windspeed']], 'pressure':row[csvDict['pressure']],'precipitation':row[csvDict['precipitation']],'humidity':row[csvDict['humidity']],'temperature':row[csvDict['temperature']],'conditions':row[csvDict['conditions']]})


def setURLDate(input, year, month, day):
    try:    
        #print('recieved URL: '+input+' replacing date with: '+str([year, month, day]))
        output = input.replace('/!YEAR*/', '/'+str(year)+'/')
        output = output.replace('/!MONTH*/', '/'+str(month)+'/')
        output = output.replace('/!DAY*/', '/'+str(day)+'/')
        output = output.replace('=!YEAR*', '='+str(year)+'&')
        output = output.replace('=!MONTH*&', '='+str(month)+'&')
        output = output.replace('=!DAY*&', '='+str(day)+'&')
        return output+'&format=1?format=1'
    except Exception,e:
        #pass
#&day=11&month=05&year=2013
        print('Failed with error: in setURLDate '+str(e))
#setURLDate("http://www.wunderground.com/history/airport/OBBI/2013/05/11/DailyHistory.html&format=1?format=1", '1999', '01', '10')

def loadWeatherData(url, circuit, dateStr):
    timeForm = 'Time'
    data = scraperwiki.scrape(url)
    reader = csv.reader(data.splitlines())
    rowCounter = -1;
    timeFound = 0
    procesList = []
    for row in reader:
        subDateStr = dateStr
        if rowCounter < 1:    
            headerCounter = 0
            for entr in row:
                try:
                    csvDict[str(nameDict[entr])] = headerCounter 
                    #if (row[0] == 'TimeAST'):
                    timeForm = str(row[0])
                    #print(timeForm)
                    headerCounter +=1
                except:
                    headerCounter +=1
                    #print('err')
            rowCounter+=1
        else:
            try:
                #print('time is '+row[0])
                if (row[0] not in ('<br>','<br />')):
                    if(timeForm in ('TimeAST', 'TimeEST', 'TimeMYT', 'TimeCST', 'TimeGST', 'TimeGMT', 'TimeBRST' ,'TimeBRT', 'TimeCEST', 'TimeSGT', 'TimeJST', 'TimeKST', 'TimeIST', 'TimeEEST', 'TimeIST', 'TimeEDT')):
                        now = (time.strptime(row[0], "%I:%M %p"))
                        if (now.tm_hour == 14):
                            timeFound = 1
                            #print('processing '+circuit+" for "+dateStr+' @'+str(now.tm_hour)+":"+str(now.tm_min).zfill(2))
                            subDateStr = dateStr+' '+str(now.tm_hour)+':'+str(now.tm_min).zfill(2)
                            #procesRow(row,circuit, subDateStr )
                            procesObj = [row]
                            procesList.append(procesObj)
                            break;
                    elif (timeForm == 'Time'):
                        now = (time.strptime(row[0], "%Y-%m-%d %H:%M:%S"))
                        if (now.tm_hour == 14):
                            timeFound = 1
                            #print('processing '+circuit+" for "+dateStr+' @'+str(now.tm_hour)+":"+str(now.tm_min).zfill(2))
                            subDateStr = dateStr+' '+str(now.tm_hour)+':'+str(now.tm_min).zfill(2)
                            #procesRow(row,circuit, subDateStr )
                            #procesObj = [row,circuit, subDateStr]
                            procesObj = [row]
                            procesList.append(procesObj)
                            break;
                    else:
                        print('********************************************************')
                        print('Timeproblems! '+timeForm)
                        print('********************************************************')
                        break;
                    
            except Exception,e: 
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                    print ('err in timeForm : '+str(e))
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    #if (len(procesList) == 0):
    if (len(procesList) > 0):
        procesRow(procesList, circuit, dateStr)
        #print('*** Did not find 14:** hour')
    #else:
        
    #print(csvDict)

trackcityDict = dict()
mech = Browser()
def setDict():
    trackcityURL = 'http://www.grandprixweather.com/F1Circuits/'
    html = mech.open(trackcityURL).read()
    soup = BeautifulSoup(html)
    table = soup.find('tbody').findAll('tr')
    for entry in table:
        trackcityDict[entry.findAll('td')[2].text]= entry.findAll('td')[0].text
    
    print('finished track-city dictionary')
    print (trackcityDict)

circuitList = []
def procesWeather(year):

    calUrl= 'http://www.gpupdate.net/nl/kalender/110/formule-1-kalender-2010/'
    page = mech.open(calUrl)
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.findAll("div",{"class" : "section_container"})[1].find('table').findAll('td')
    monthDict = dict(jan=1, feb=2, mrt=3, apr=4, mei=5, jun=6, jul=7, aug=8, sep=9, okt=10,nov=11, dec=12)
    
    seasonArr = []
    tracksArr = []
    
    for ent in table:
        try:
            tempArr = [ent.text, ent.a.get('href')]
            seasonArr.append(tempArr)
        except:
            pass
    masterCalendar = []
    for ent in seasonArr:
        
        #print('season: '+str(ent[0]))
        #if (int(ent[0])>1998): 
        if (int(ent[0])==year): 
            page = mech.open(ent[1]).read()
            soup = BeautifulSoup(page)   
            try:
                table = soup.find("div",{"id" : "middle_container"}).findAll('tr')
            except Exception,e: 
                print ('!!! Could not open url for season: '+ent[1]+' with error: '+str(e))
            for subEnt in table:
                try:
                    tds = subEnt.findAll('td')
                    try: 
                        trackname = tds[2].text
                        if (trackname.encode('utf-8') == 'Nürburgring'):
                            trackname = 'Nurburgring'
                            #print (trackname.encode('utf-8') == 'Nürburgring')
                        #print(tds[2].text)
                        #print(tds[2].text.encode('utf-8'))  
                        #tracksArr[tds[2].text].append(tds[0].text)
                        v = re.search('([0-9]{1,2})[ /t]([a-z]{3})[ /t]([0-9]{4})',tds[0].text)
                        day = str(v.group(1))
                        month = str(monthDict[v.group(2)])
                        year = str(v.group(3))
                        tempArr = [tds[2].text,day,month,year]
                    except Exception,e:
                        #pass
                        print('Failed with error: in getDates setting Date var '+str(e))
                        #break;
                    try:  
                        url = setURLDate(str(trackURLDict[trackname]), str(year), str(month), str(day))
                        print(trackname +": "+str(day)+"/"+str(month)+"/"+str(year)+" url: "+url )
                    except Exception,e:
                        #pass
                        print('Failed with error: in getDates setting URL '+str(e))
                    
                    try:
                        datVar = str(year)+'-'+str(month)+'-'+str(day);
                    except Exception,e:
                        #pass
                        print('Failed with error: in getDates setting datVar '+str(e)+' on '+str(year)+' '+trackname)
                    
                    try:  
                        loadWeatherData(url,trackname , datVar)
                        circuitList.append(trackname)
                    except Exception,e:
                        #pass
                        print('Failed with error: in getDates calling loadWeatherData '+str(e)+' on '+str(year)+' '+trackname) 
                except Exception,e:
                    #pass
                    print('Failed with error: in getDates '+str(e))
            #break;

            #break;

def flatten(el):          
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)



#get races from year
#<li class="listheader"><span><a href="/results/season/2012/">
#www.formula1.com/results/season/2012/





#,["http://www.formula1.com/results/season/2011/848/6835/","CHINA"]

#http://www.formula1.com/results/season/2011/844/6825/fastest_laps.html

def dropper(table):
    if nodrop==1: return
    print "dropping",table
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass



#Preferred time format
def formatTime(t):
    return float("%.3f" % t)
# Accept times in the form of hh:mm:ss.ss or mm:ss.ss
# Return the equivalent number of seconds
def getTime(ts):
    tm=''
    if ts.find(':')>-1:
        t=ts.strip()
        t=ts.split(':')
        if len(t)==3:
            tm=60*int(t[0])+60*int(t[1])+float(t[2])
        elif len(t)==2:
            tm=60*int(t[0])+float(t[1])
        tm=formatTime(tm)
    else:
        try:
            tm=float(ts)
            tm=formatTime(tm)
        except:tm=''
    return tm

def qSpeedScraper(sessions,tn,year):    
    dropper(tn)
    bigdata=[]
    for quali in sessions:
        url=quali[0]+'speed_trap.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4])]
                    #writer.writerow(data)
                    data={'year':year,'race':quali[1], 'circuit': tracknameDict[quali[2]], 'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'timeOfDay':flatten(cells[3]),'qspeed':flatten(cells[4])}
                    bigdata.append(data.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)


def qSectorsScraper(sessions,tn,year):
    dropper(tn)
    bigdata=[]
    for quali in sessions:
        url=quali[0]+'best_sector_times.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            sector=0
            for table in page.findall('.//table'):
                sector=sector+1
                for row in table.findall('.//tr')[2:]:
                    #print row,flatten(row)
                    cells=row.findall('.//td')
                    #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),sector,flatten(cells[3])]
                    #writer.writerow(data)
                    data={'year':year,'race':quali[1], 'circuit':tracknameDict[quali[2]], 'pos':flatten(cells[0]),'driverNum':flatten(cells[1]),'driverName':flatten(cells[2]),'sector':sector,'sectortime':flatten(cells[3])}
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    bigdata.append(data.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    #fout.close()
    
def qResults(qualis,year):
    tn='qualiResults'
    dropper(tn)
    dropper('sessionResults')
    bigdata=[]
    bigSessionData=[]
    for quali in qualis:
        url=quali[0]+'results.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            if (tracknameDict[quali[2]].encode('utf-8') == 'Nürburgring'):
                trackname = 'Nurburgring'
            else:
                trackname = tracknameDict[quali[2]];

            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    if flatten(cells[0])=='':continue
                    #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                    #writer.writerow(data)
                    try:
                        data={'year':year,'race':quali[1], 'circuit':trackname, 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'q1natTime':flatten(cells[4]), 'q1time':getTime(flatten(cells[4])), 'q2natTime':flatten(cells[5]), 'q2time':getTime(flatten(cells[5])), 'q3natTime':flatten(cells[6]), 'q3time':getTime(flatten(cells[6])), 'qlaps':flatten(cells[7])}
                    except Exception,e: 
                        print('Error setting data: '+str(e)+' at '+str(url)+' - '+str(row))

                    try:
                        if (flatten(cells[4]) != ''):
                            timeGap= flatten(cells[4])
                            session = 'Q1'
                            sessionData={'circuit':trackname,'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':quali[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[7]), 'timeGap':timeGap, 'session':session}
                            bigSessionData.append(sessionData.copy())
                    except Exception,e: 
                        print('Error setting Q1: '+str(e)+' at '+str(url)+' - '+str(row))

                    try:
                        if(flatten(cells[5]) != ''):
                            timeGap= flatten(cells[5])
                            session = 'Q2'
                            sessionData={'circuit':trackname,'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':quali[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[7]), 'timeGap':timeGap, 'session':session}
                            bigSessionData.append(sessionData.copy())
                    except Exception,e: 
                        print('Error setting Q2: '+str(e)+' at '+str(url)+' - '+str(row))
                        continue

                    try:
                        if (flatten(cells[6]) != ''):
                            timeGap= flatten(cells[6])
                            session = 'Q3'
                            sessionData={'circuit':trackname,'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':quali[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[7]), 'timeGap':timeGap, 'session':session}
                            bigSessionData.append(sessionData.copy())
                    except Exception,e:
                        print('Error setting Q3: '+str(e)+' at '+str(url)+' - '+str(row))
                        continue
                    
                    sessionData={'circuit':trackname,'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':quali[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[7]), 'timeGap':timeGap, 'session':'Q results'}
                    bigSessionData.append(sessionData.copy())
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    bigdata.append(data.copy())

                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
                        scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=1)
                        bigSessionData=[]
        except Exception,e: 
            print ("This didn't work" + url + 'with err: '+str(e))
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=1)

def practiceResults(sessions,tn,year,sessionName):
    dropper(tn)
    bigdata=[]
    bigSessionData=[]
    for session in sessions:
        url=session[0]+'results.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    #data=[quali[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),getTime(flatten(cells[4])),flatten(cells[5]),getTime(flatten(cells[5])),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7])]
                    #writer.writerow(data)
                    if flatten(cells[0])=="1":
                        gap=0
                        natGap=0
                    else:
                        natGap=flatten(cells[5])
                        gap=getTime(flatten(cells[5]))
                    data={'year':year,'race':session[1], 'circuit':tracknameDict[session[2]], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'natTime':flatten(cells[4]), 'time':getTime(flatten(cells[4])), 'natGap':natGap, 'gap':gap, 'laps':flatten(cells[6])}
                    if (flatten(cells[0]) == '1'):
                        timeGap = flatten(cells[4])
                    else:
                        timeGap = '+'+natGap
                    sessionData={'circuit':tracknameDict[session[2]],'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':session[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[6]), 'timeGap':timeGap, 'session':sessionName}
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    bigdata.append(data.copy())
                    bigSessionData.append(sessionData.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
                        scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=0)
                        bigSessionData=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=0)

def resScraper(races,year):
    tn='raceResults'
    dropper(tn)
    bigdata=[]
    bigSessionData=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'results.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),flatten(cells[7])]
                    #writer.writerow(data)
                    data={'year':year,'raceNum':raceNum, 'race':race[1], 'circuit':tracknameDict[race[2]], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'laps':flatten(cells[4]), 'timeOrRetired':flatten(cells[5]), 'grid':flatten(cells[6]), 'points':flatten(cells[7])}
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    session = 'RACE'
                    sessionData={'circuit':tracknameDict[race[2]],'driverName':flatten(cells[2]), 'driverNum':flatten(cells[1]), 'pos':flatten(cells[0]), 'race':race[1], 'season':year, 'team':flatten(cells[3]), 'laps':flatten(cells[4]), 'timeGap':flatten(cells[5]), 'session':session}
                    bigdata.append(data.copy())
                    bigSessionData.append(sessionData.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
                        scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=0)
                        bigSessionData=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['circuit','season','session','driverName'], table_name='sessionResults', data=bigSessionData,verbose=0)
    #fout.close()

def pitScraper(races,year):
    tn='racePits'
    dropper(tn)
    bigdata=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'pit_stop_summary.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    #data=[race[1],flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3]),flatten(cells[4]),flatten(cells[5]),flatten(cells[6]),getTime(flatten(cells[6])),flatten(cells[7]),getTime(flatten(cells[7]))]
                    #writer.writerow(data)
                    data={'year':year,'raceNum':raceNum,'race':race[1], 'circuit':tracknameDict[race[2]], 'stops':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'natPitTime':flatten(cells[6]), 'pitTime':getTime(flatten(cells[6])), 'natTotalPitTime':flatten(cells[7]), 'totalPitTime':getTime(flatten(cells[7]))}
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    bigdata.append(data.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

def flapScraper(races,year):
    tn='raceFastlaps'
    dropper(tn)
    bigdata=[]
    raceNum=0
    for race in races:
        raceNum=raceNum+1
        url=race[0]+'fastest_laps.html'
        #print 'trying',url
        try:
            content=urllib.urlopen(url).read()
            page=lxml.html.fromstring(content)
            for table in page.findall('.//table'):
                for row in table.findall('.//tr')[1:]:
                    #print flatten(row)
                    cells=row.findall('.//td')
                    data={'year':year,'raceNum':raceNum,'race':race[1], 'circuit':tracknameDict[race[2]], 'pos':flatten(cells[0]), 'driverNum':flatten(cells[1]), 'driverName':flatten(cells[2]), 'team':flatten(cells[3]), 'lap':flatten(cells[4]), 'timeOfDay':flatten(cells[5]), 'speed':flatten(cells[6]), 'natTime':flatten(cells[7]), 'stime':getTime(flatten(cells[7]))}
                    #scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=data)
                    bigdata.append(data.copy())
                    if len(bigdata)>1000:
                        scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)
                        bigdata=[]
        except:
            print "This didn't work",url
    scraperwiki.sqlite.save(unique_keys=[], table_name=tn, data=bigdata,verbose=0)

mech = Browser()
calendarDict = {'12/05/20013':'Circuit de Catalunya', '27/11/2011':'Interlagos', '07/11/2010':'Interlagos'}
def getDates(y):
    url= 'http://www.gpupdate.net/nl/kalender/178/formule-1-kalender-2013/'
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.findAll("div",{"class" : "section_container"})[1].find('table').findAll('td')
    monthDict = dict(jan=1, feb=2, mrt=3, apr=4, mei=5, jun=6, jul=7, aug=8, sep=9, okt=10,nov=11, dec=12)
    seasonArr = []
    tracksArr = []
    for ent in table:
        try:
            tempArr = [ent.text, ent.a.get('href')]
            seasonArr.append(tempArr)
        except:
            pass
    
    masterCalendar = []
    for ent in seasonArr:
        if (int(ent[0])==int(y)): 
            page = mech.open(ent[1]).read()
            soup = BeautifulSoup(page)   
            try:
                table = soup.find("div",{"id" : "middle_container"}).findAll('tr')
            except Exception,e: 
                print ('!!! Could not open url for season: '+ent[1]+' with error: '+str(e))
            nur = 'nürburgring'
            #print(str(nur))
            for subEnt in table:
                try:    
                    tds = subEnt.findAll('td')
                    trackname = tds[2].text
                    if (trackname.encode('utf-8') == 'Nürburgring'):
                        trackname = 'Nurburgring'
                        #print (trackname.encode('utf-8') == 'Nürburgring')
                    #print(tds[2].text)
                    #print(tds[2].text.encode('utf-8'))  
                    #tracksArr[tds[2].text].append(tds[0].text)
                    v = re.search('([0-9]{1,2})[ /t]([a-z]{3})[ /t]([0-9]{4})',tds[0].text)
                    day = str(v.group(1))
                    month = str(monthDict[v.group(2)])
                    year = str(v.group(3))
                    tempArr = [tds[2].text,day,month,year]
                    #masterCalendar.append(tempArr)
    #                    url = setURLDate(str(trackURLDict[trackname]), str(year), str(month), str(day))
                    datVar = str(day).zfill(2)+'/'+str(month).zfill(2)+'/'+str(year);
                    calendarDict[datVar] = tds[2].text
                    #print(datVar+' - '+tds[2].text)
                except Exception,e:
                    #pass
                    print('Failed with error: in getDates '+str(e)+' season: '+ent[1])



nodrop=1
latest=0
scraping=7

def liaparse(ul):
    d=[]
    lis=ul.findall('.//li')
    for li in lis:
        a=li.find('a')
        u=a.get('href')
        r=flatten(li)
        #print u,r
        d.append((u,r))
    return d

#import mechanize


def yearGrabber(year, raceNum):
    getDates(year)
    #print(calendarDict)
    seasonTrackArr= []
    urlstub='http://www.formula1.com/results/season'
    url='/'.join( [urlstub,str(year) ])
    #print 'trying',url
    content=urllib.urlopen(url).read()
    page=lxml.html.fromstring(content)
    uls =page.findall('.//ul')
    trs = page.findall('.//tr')
    print('******* trs')
    #print(trs)
    #counter = 0;
    start = raceNum
    end = raceNum+1
    #for el in trs[1:]:
    for el in trs[start:end]:
        print('el in trs')
        print calendarDict[flatten(el[1])]
        trackName = calendarDict[flatten(el[1])]
        seasonTrackArr.append(trackName)
        #counter +=1
        #for some in el:
    #lis=uls[14].findall('.//li')
    ah=liaparse(uls[14])
    #for li in lis[1:]:
    #    a=li.find('a')
    #    u=a.get('href')
    #    r=flatten(li)
    #    print u,r
    s1=[]
    s2=[]
    s3=[]
    qualis=[]
    races=[]
    counter = 0;
    #for (u,r) in ah[1:]:
    for (u,r) in ah[start:end]:
        
        #print 'u,r: '+u,r
        #print 'trying',u
        #print('I think this is '+seasonTrackArr[counter])
        

        content2=urllib.urlopen('http://formula1.com'+u).read()

        #br = mechanize.Browser()
        #response = br.open(url)
        #content=response.read()
        page2=lxml.html.fromstring(content2)
        uls2 =page2.findall('.//ul')
        #print len(uls2),content

        ah2=liaparse(uls2[15])
        for (u2,r2) in ah2:
            #print '\t',u2,r2
            if '1' in r2:
                s1.append(['http://formula1.com'+u2,r.strip(),seasonTrackArr[counter]])
            elif '2' in r2:
                s2.append(['http://formula1.com'+u2,r.strip(),seasonTrackArr[counter]])
            elif '3' in r2 or 'SATURDAY' in r2:
                s3.append(['http://formula1.com'+u2,r.strip(),seasonTrackArr[counter]])
            elif 'QUALI' in r2:
                qualis.append(['http://formula1.com'+u2,r.strip(),seasonTrackArr[counter]])
            elif 'RACE' in r2:
                races.append(['http://formula1.com'+u2,r.strip(),seasonTrackArr[counter]])
        #print s1,s2,s3,qualis,races
        counter +=1
        #exit(-1)
    #exit(-1)
    if scraping==1:scrapeset=["P1","P2","P3"]
    if scraping==2:scrapeset=["P1","P2"]
    if scraping==3:scrapeset=["P3"]
    if scraping==4:scrapeset=["P3","Q"]
    if scraping==5:scrapeset=["Q"]
    if scraping==6:scrapeset=["R"]
    if scraping==7:scrapeset=["P1","P2","P3","Q","R"]

    #Practice: best_sector_times.html, speed_trap.html
    #s1=[]
    if (latest==1): s1=[s1[-1]]
    #s2=[]
    if (latest==1): s2=[s2[-1]]
    #s3=[]
    if (latest==1): s3=[s3[-1]]

    #best_sector_times.html, speed_trap.html, results.html
    #qualis=[]
    if (latest==1): qualis=[qualis[-1]]

    #pit_stop_summary.html, fastest_laps.html, results.html
    #races=[]
    if (latest==1): races=[races[-1]]

    #print ("Race")
    if "R" in scrapeset:
        flapScraper(races,year)
        resScraper(races,year)
        pitScraper(races,year)

    #print("Quali")
    if "Q" in scrapeset:
        qSpeedScraper(qualis,'qualiSpeeds',year)
        qResults(qualis,year)
        qSectorsScraper(qualis,'qualiSectors',year)


    #print("P1")
    if "P1" in scrapeset:
        qSpeedScraper(s1,"p1Speeds",year)
        qSectorsScraper(s1,"p1Sectors",year)
        practiceResults(s1,"p1Results",year,'FP1')

    #print("P2")
    if "P2" in scrapeset:
        qSpeedScraper(s2,"p2Speeds",year)
        qSectorsScraper(s2,"p2Sectors",year)
        practiceResults(s2,"p2Results",year,'FP2')

    #print("P3")
    if "P3" in scrapeset:
        qSpeedScraper(s3,"p3Speeds",year)
        qSectorsScraper(s3,"p3Sectors",year)
        practiceResults(s3,"p3Results",year,'FP3')

#procesWeather()
for y in ['2013']:#, '2012', '2011', '2010', '2009', '2008', '2007']:#, '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996','1995','1994','1993','1992','1991','1990', '1989', '1988']:
    yearGrabber(y,10)
    procesWeather(y)
exit(-1)

