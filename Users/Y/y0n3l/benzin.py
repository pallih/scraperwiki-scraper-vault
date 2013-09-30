import scraperwiki
from scrapemark import scrape
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import json
import urllib
import urllib2
# Blank Python

TYPE_DIESEL = "DIE"
TYPE_SUPER = "SUP"

def getSubRegions():
    result = []
    response = urllib2.urlopen('http://www.spritpreisrechner.at/ts/BezirkServlet')
    html = response.read()
    regionen = scrape("""
        regionen={ {{  }} }};
        """,
        html)
    regionen = "{" + regionen + "}}"
    regionenDict = json.loads(regionen)
    #print "REGIONEN %s " % jsonRegionen 
    for region in regionenDict.keys():
        info = regionenDict[region]
        unterregionen = info['unterregionen']
        for unterregion in unterregionen:
            unterregionName = unterregion ['bezeichnung']
            code = unterregion ['code']
            #print "%s / %s %s" % (region, unterregionName, code)
            result.append({"code":code, "region":region, "name":unterregionName})
    return result
        

def syncPricesFor(subRegionCode, gasType):
    #print "======= NOW GETTING %s FROM %s ========" % (gasType, subRegionCode) 
    html = None
    query_args = {'data': '["%s","PB","%s","checked"]' % (subRegionCode, gasType) }
    data = urllib.urlencode(query_args)
    req = urllib2.Request("http://www.spritpreisrechner.at/ts/BezirkStationServlet", data)
    response = urllib2.urlopen(req)
    jsonResult = response.read()
    result = json.loads(jsonResult)        
    #print "result %s" % (result)
    for station in result:
        latitude = station['latitude']
        longitude = station['longitude']
        zipCode = station ['postalCode']
        name = station ['gasStationName']
        address = station ['address']
        city = station ['city']
        price = station ['spritPrice'][0]['amount']
        gasStation = {"name":name, "address":address, "zipcode":zipCode, "city":city, "latitude":latitude, "longitude":longitude, gasType:price}
        #print "EXTRACTED %s" % gasStation

        try:
            # encode params in case name or address contains a " ' etc...
            existing = scraperwiki.sqlite.select("* from swdata where name=? AND address=?", [name, address])[0] 
            if existing:
                if existing[TYPE_DIESEL]==None:
                    del existing[TYPE_DIESEL]
                if existing[TYPE_SUPER]==None:
                    del existing[TYPE_SUPER]
                                
                #print "gasStation %s" % (gasStation)
                #print "existing %s" %  (existing)
                gasStation.update(existing)
                #print "result %s" % gasStation
        except:
            pass
        scraperwiki.sqlite.save(unique_keys=["name", "address"], data= gasStation)

allSubRegions=getSubRegions()
index = 1
total = len(allSubRegions)
for subRegion in allSubRegions:
    subRegionCode = subRegion["code"]
    print "[%d/%d] Syncing prices for %s / %s (%s)" % (index, total, subRegion["region"], subRegion["name"], subRegionCode)  
    syncPricesFor(subRegionCode, TYPE_SUPER)
    syncPricesFor(subRegionCode, TYPE_DIESEL)
    index = index+1

import scraperwiki
from scrapemark import scrape
from datetime import datetime, date
from httplib import IncompleteRead
from lxml.html.soupparser import fromstring
from os import path
from urllib2 import URLError
import os.path
import json
import urllib
import urllib2
# Blank Python

TYPE_DIESEL = "DIE"
TYPE_SUPER = "SUP"

def getSubRegions():
    result = []
    response = urllib2.urlopen('http://www.spritpreisrechner.at/ts/BezirkServlet')
    html = response.read()
    regionen = scrape("""
        regionen={ {{  }} }};
        """,
        html)
    regionen = "{" + regionen + "}}"
    regionenDict = json.loads(regionen)
    #print "REGIONEN %s " % jsonRegionen 
    for region in regionenDict.keys():
        info = regionenDict[region]
        unterregionen = info['unterregionen']
        for unterregion in unterregionen:
            unterregionName = unterregion ['bezeichnung']
            code = unterregion ['code']
            #print "%s / %s %s" % (region, unterregionName, code)
            result.append({"code":code, "region":region, "name":unterregionName})
    return result
        

def syncPricesFor(subRegionCode, gasType):
    #print "======= NOW GETTING %s FROM %s ========" % (gasType, subRegionCode) 
    html = None
    query_args = {'data': '["%s","PB","%s","checked"]' % (subRegionCode, gasType) }
    data = urllib.urlencode(query_args)
    req = urllib2.Request("http://www.spritpreisrechner.at/ts/BezirkStationServlet", data)
    response = urllib2.urlopen(req)
    jsonResult = response.read()
    result = json.loads(jsonResult)        
    #print "result %s" % (result)
    for station in result:
        latitude = station['latitude']
        longitude = station['longitude']
        zipCode = station ['postalCode']
        name = station ['gasStationName']
        address = station ['address']
        city = station ['city']
        price = station ['spritPrice'][0]['amount']
        gasStation = {"name":name, "address":address, "zipcode":zipCode, "city":city, "latitude":latitude, "longitude":longitude, gasType:price}
        #print "EXTRACTED %s" % gasStation

        try:
            # encode params in case name or address contains a " ' etc...
            existing = scraperwiki.sqlite.select("* from swdata where name=? AND address=?", [name, address])[0] 
            if existing:
                if existing[TYPE_DIESEL]==None:
                    del existing[TYPE_DIESEL]
                if existing[TYPE_SUPER]==None:
                    del existing[TYPE_SUPER]
                                
                #print "gasStation %s" % (gasStation)
                #print "existing %s" %  (existing)
                gasStation.update(existing)
                #print "result %s" % gasStation
        except:
            pass
        scraperwiki.sqlite.save(unique_keys=["name", "address"], data= gasStation)

allSubRegions=getSubRegions()
index = 1
total = len(allSubRegions)
for subRegion in allSubRegions:
    subRegionCode = subRegion["code"]
    print "[%d/%d] Syncing prices for %s / %s (%s)" % (index, total, subRegion["region"], subRegion["name"], subRegionCode)  
    syncPricesFor(subRegionCode, TYPE_SUPER)
    syncPricesFor(subRegionCode, TYPE_DIESEL)
    index = index+1

