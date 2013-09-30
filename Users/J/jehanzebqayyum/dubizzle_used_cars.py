#!/usr/bin/env python

import scraperwiki
import re
import pytz
from datetime import datetime, date, time
from pyquery import PyQuery as pq
import sqlite3
import pickle

def isCarStatTableExist():
    tablesInfo = scraperwiki.sqlite.show_tables()
    print tablesInfo
    if 'car_stat' in tablesInfo:
        return True
    else:
        return False
    
    
def createCarStatTable():
    scraperwiki.sqlite.execute("create table car_stat (make string, model string, year int, price int, color string,\
        mileage string, advert_date date, created_on datetime, primary key (make,model,year,price,color,mileage,advert_date))")
        

def saveCarStat(carStat):
    try:
        scraperwiki.sqlite.execute("insert into car_stat values (?,?,?,?,?,?,?,?)", (carStat["make"], carStat["model"], carStat["year"], 
            carStat["price"], carStat["color"], carStat["mileage"], pickle.dumps(carStat["advert_date"]),
             pickle.dumps(datetime.now(pytz.timezone('Asia/Dubai')))))
        return True
    except Exception,e:
        print "error:", str(e) 
        return False
    
def getCarMake(makeAndModel):
    make = ""
    matcher = re.search(".+>(.+)>.+", makeAndModel)
    if matcher:
        make = matcher.group(1)
    return removeNonAscii(re.sub("\s", "", make))
    
def getCarModel(makeAndModel):
    model = ""
    matcher = re.search(".+>.+>(.+)", makeAndModel)
    if matcher:
        model = matcher.group(1)
    return removeNonAscii(re.sub("\s", "", model))

def getNumber(text):
    return re.sub("\D", "", text)
    

def getDate(dateText):
    dateComps = dateText.strip().split(" ")
    normalizedDate = getNumber(dateComps[0]) + " " + dateComps[1] + " " + dateComps[2]
    return datetime.strptime(normalizedDate, "%d %B %Y").date()

def getColor(colorText):
    color = ""
    matcher = re.search("color: (.+)", colorText)
    if matcher:
        color = matcher.group(1)
    return color.strip()

    
def extractCarFeatures(carStat, featureText):
    featureText = featureText.lower()
    if "year" in featureText:
        carStat["year"] = getNumber(featureText)
    elif "kilometers" in featureText:
        carStat["mileage"] = getNumber(featureText);
    elif "color" in featureText:
        carStat["color"] = getColor(featureText)

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)


#if not isCarStatTableExist():
#    createCarStatTable()

maxPage = 40
pagesFetched = 0
savedItemsCount = 0
shouldExit = False

for page in range(1,maxPage+1):
    print "fetching page " + str(page) + " ..."
    usedCarPage = pq(url="http://dubai.dubizzle.com/motors/used-cars/?page="+str(page))
    pagesFetched += 1    
    itemsList = usedCarPage('.listing-item')
  
    for item in itemsList:
        carStat = {}
        carStat["make"] = getCarMake(pq(item)(".breadcrumbs").text())
        carStat["model"] = getCarModel(pq(item)(".breadcrumbs").text())
        carStat['price'] = getNumber(pq(item)(".price").text())
        carStat['advert_date'] = getDate(pq(item)(".date").text())
        for ul in pq(item)(".features"):
            for li in pq(ul)("li"):
                extractCarFeatures(carStat,pq(li).text())
    
        if saveCarStat(carStat):
            savedItemsCount += 1    
        else:
            shouldExit = True
            break
    
    if shouldExit:
        break
    
scraperwiki.sqlite.commit()
print "pagesFetched: " + str(pagesFetched)
print "savedItemsCount: " + str(savedItemsCount)
