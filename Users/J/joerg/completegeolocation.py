import scraperwiki
import sys
import urllib
from urllib import urlencode
import urllib2
from urlparse import urlparse
import json
import csv
import re
import simplejson
import time
from geopy.geocoders.base import Geocoder
from geopy.util import logger, decode_page, join_filter

scraperwiki.sqlite.attach("skillcheck_with_fixed_array")

# CHECK: Integrate duplicates (same company and region)
# TODO: Integrate data from company_data1-5 into company_data (rename company_data, create company_data, copy cd5, check rows from other company_data)
#scraperwiki.sqlite.execute("ALTER TABLE company_data RENAME TO company_data1")
#scraperwiki.sqlite.execute("ALTER TABLE company_data5 RENAME TO company_data")
#scraperwiki.sqlite.execute("drop table if exists company_data1")
#scraperwiki.sqlite.execute("drop table if exists company_data2")
#scraperwiki.sqlite.execute("drop table if exists company_data3")
#scraperwiki.sqlite.execute("drop table if exists company_data4")
#scraperwiki.sqlite.execute("drop table if exists company_data5")

# TODO: handle semantical duplicates ("Berlin" vs "Berlin, Germany") (by distance of geo-coord? using a file with cities (Berlin, New York, ...)?)
test = scraperwiki.sqlite.select("region FROM company_data5 WHERE region LIKE '%Berlin%' GROUP BY region")
print test
for row in test:
    print row

#scraperwiki.sqlite.execute("drop table if exists company_data5")
try:    scraperwiki.sqlite.execute("create table company_data5 (oldID, id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'company_data5' already exists."

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass

count = 0
#skip: companies  = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A")
companies = []
for record in companies:
    count = count + 1
    if count%1000 == 0: print count, " jobs processed."

    try:
        dataAlreadySaved = scraperwiki.sqlite.select("id from company_data5 where oldID='"+record["oldID"]+"'", verbose=0)
        if dataAlreadySaved: continue
    except: pass

    regionList = []
    regionText = record["region"]
    record["orginalRegion"] = record["region"]
    
    if regionText.endswith("USA") or regionText.endswith(", NY"):
        record["region"] = record["region"].replace("Us - Ca - ", "").replace("Usa-ca-", "")
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
        continue
    if "PLZ"          in regionText: continue
    if "Postleitzahl" in regionText: continue
    if "keine"        == regionText: continue

    if   regionText.count(',') >= 4: regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " und " in regionText:
        regionText = regionText.replace(" und ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " & " in regionText:
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " sowie " in regionText:
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " oder " in regionText:
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " und/oder " in regionText:
        regionText = regionText.replace(" und/oder ", ",")
        regionList = regionText.split(',') 
    elif regionText.count(',') >= 1 and " and " in regionText:
        regionText = regionText.replace(" and ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" or ",     ",")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " or " in regionText:
        regionText = regionText.replace(" and ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" or ",     ",")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " and/or " in regionText:
        regionText = regionText.replace(" and/or ", ",")
        regionList = regionText.split(',') 
    elif regionText.count(',') >= 2 and "/" in regionText:
        regionList = regionText.split(',') 

    elif regionText.count('/') >= 2: 
        regionList = regionText.split('/')
        for fragment in regionList:
            if fragment.count('-') >= 2:
                regionList.extend(fragment.split('-'))
    elif regionText.count('/') >= 1 and " und " in regionText:
        regionText = regionText.replace(" und ",      "/")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     "/")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " oder " in regionText:
        regionText = regionText.replace(" und ",      "/")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     "/")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " und/oder " in regionText:
        regionText = regionText.replace(" und/oder ", "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " and " in regionText:
        regionText = regionText.replace(" and ",      "/")
        regionText = regionText.replace(" or ",       "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " or " in regionText:
        regionText = regionText.replace(" and ",      "/")
        regionText = regionText.replace(" or ",       "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " and/or " in regionText:
        regionText = regionText.replace(" and/or ",   "/")
        regionList = regionText.split('/') 

#-
    elif regionText.count(';') >= 2: regionList = regionText.split(';')
    elif "\u2022" in regionText:     regionList = regionText.split('\u2022')
    elif "+" in regionText:          regionList = regionText.split('+')
    elif "+++" in regionText:        regionList = regionText.split('+++')
    elif " - " in regionText:        regionList = regionText.split(' - ')
    elif " oder " in regionText:     regionList = regionText.split(' oder ')
    elif " ODER " in regionText:     regionList = regionText.split(' ODER ')
    elif " bzw. " in regionText:     regionList = regionText.split(' bzw. ')
    elif " und " in regionText:      regionList = regionText.split(' und ')
    elif " UND " in regionText:      regionList = regionText.split(' UND ')
    elif " & " in regionText:        regionList = regionText.split(' & ')
    elif " sowie " in regionText:    regionList = regionText.split(' sowie ')
    elif " und/oder " in regionText: regionList = regionText.split(' und/oder ')
    elif " and " in regionText:      regionList = regionText.split(' and ')
    elif " or " in regionText:       regionList = regionText.split(' or ')
    elif " and/or " in regionText:   regionList = regionText.split(' and/or ')
    else:
        regionText = " ".join(regionText.strip().split())
        if   regionText.count(' ') >= 6: regionList = regionText.split(' ') #3
        elif regionText.count(',') >= 3: regionList = regionText.split(',')

    if regionList != []:
        regionList = list(set(regionList))
        record["oldID"] = record["id"]
#        print regionList, regionText
    else:
        for phrase in redundantText:
            record["region"] = record["region"].replace(phrase, " ")
        regionName = record["region"].strip()
        regionName = " ".join(regionName.split())
        regionName = regionName[:-1]  if regionName.endswith(',')   else regionName
        regionName = regionName[:-1]  if regionName.endswith('.')   else regionName
        regionName = regionName[1:-1] if regionName.startswith('(') and regionName.endswith(')')   else regionName
        regionName = regionName[:-1]  if regionName.endswith('(')   else regionName
        regionName = regionName[:-1]  if regionName.endswith(')')   and regionName.count("(") == 0    else regionName
#        regionName = regionName[1:]  if regionName.startswith('(') else regionName
        regionName = regionName[:-1]  if regionName.endswith('-')   else regionName
        regionName = regionName[1:]   if regionName.startswith('-') else regionName
        regionName = regionName.replace("( ","(").replace("/ ","/")
        if len(regionName) <= 2: continue
        regionName = " ".join(regionName.split())
        if regionName == "Esse":    regionName = "Essen"
        if len(regionName.replace("(","").replace(")","").replace("-","")) <= 2: continue
        record["region"]     = regionName
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
        continue

    regionCount = 1
    orgID = record["id"]
    for region in regionList:
        for phrase in redundantText:
            region = region.replace(phrase, " ")
        regionName = region.strip() #.replace("(","").replace(")","")
        regionName = " ".join(regionName.split())
        regionName = regionName[:-1] if regionName.endswith(',')   else regionName
        regionName = regionName[:-1] if regionName.endswith(',')   else regionName
        regionName = regionName[1:-1] if regionName.startswith('(') and regionName.endswith(')')   else regionName
        regionName = regionName[:-1] if regionName.endswith('(')   else regionName
        regionName = regionName[:-1] if regionName.endswith(')') and regionName.count("(") == 0    else regionName
#        regionName = regionName[1:]  if regionName.startswith('(') else regionName
        regionName = regionName[:-1] if regionName.endswith('-')   else regionName
        regionName = regionName[1:]  if regionName.startswith('-') else regionName
        regionName = regionName.replace("( ","(").replace("/ "," / ")
        regionName = " ".join(regionName.split())
        if len(regionName.replace("(","").replace(")","").replace("-","")) <= 2: continue
        if regionName == "oder":    continue
        if regionName == "von":     continue
        if regionName == "vor":     continue
        if regionName == "den":     continue
        if regionName == "mit":     continue
        if regionName == "f\u00fcr": continue
        if regionName == "für":     continue
        if regionName == "S\u00fcd": continue
        if regionName == "Augsbur": regionName = "Augsburg"
        if regionName == "Hambu":   regionName = "Hamburg"
        if regionName == "Esse":    regionName = "Essen"
        record["region"]     = regionName
        record["oldID"]      = orgID 
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)

#sys.exit()

mapquest_baseurl   = "http://open.mapquestapi.com/nominatim/v1/search?format=json&q="
googlemaps_baseurl = "http://maps.google.com/maps/api/geocode/json?sensor=false&address="
bingmaps_baseurl   = "http://dev.virtualearth.net/REST/v1/Locations?key=AiAuYPgWdmuTp4M5iPrPgw25Be4akjr2cWif56FDqM7mOVhSawBjMkoPoxop_wma&q="

#scraperwiki.sqlite.execute("drop table if exists company_data5")
try:    scraperwiki.sqlite.execute("create table company_data5 (id)")
except: print "Table 'company_data5' already exists."

#scraperwiki.sqlite.attach("skillcheck_with_fixed_array")
#companies  = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A WHERE NOT EXISTS(SELECT NULL FROM company_data5 AS B WHERE A.id=B.id)")
#companies = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A WHERE     EXISTS(SELECT NULL FROM company_data5 AS B WHERE A.id=B.id) ORDER BY A.company ASC")
companies  = scraperwiki.sqlite.select("* FROM company_data5 WHERE longitude = '' OR longitude IS NULL")
print "Total number of companies not geolocated:  ", len(companies)

# Start
count = 0
for record in companies:
#    if record["region"] == None: 
#        continue

    count = count + 1
    if count%1000 == 0: print count, " jobs processed."

    geocodeFound = False

    try: #check if geocode was already requested
        alreadyGeocoded = ""
        alreadyGeocoded = scraperwiki.sqlite.select("latitude, longitude FROM company_data5 WHERE region=? AND latitude IS NOT NULL LIMIT 1", (record["region"]), verbose=0)
        if alreadyGeocoded: 
            try:    record["latitude"]  = alreadyGeocoded[0]["latitude"]
            except: pass
            try:    record["longitude"] = alreadyGeocoded[0]["longitude"]
            except: pass
            try:    record["geoSource"] = alreadyGeocoded[0]["geoSource"]
            except: pass
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except:
        print sys.exc_info() # pass
    if geocodeFound: continue

    try: # ask google maps to geolocate
        geocode_url = googlemaps_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
            record["geoSource"] = "GoogleMaps"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: pass
    if geocodeFound: continue

    try: # ask bing maps to geolocate
        geocode_url = bingmaps_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]    = geodata["resourceSets"][0]["resources"][0]["point"]["coordinates"][0]
            record["longitude"]   = geodata["resourceSets"][0]["resources"][0]["point"]["coordinates"][1]
            record["geoSource"] = "BingMaps"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: pass
    if geocodeFound: continue

    try: # ask mapquest to geolocate
        geocode_url = mapquest_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
#        geocode_url = mapquest_baseurl + urllib.quote_plus(urllib.quote(record["region"].encode('utf-8')))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]  = geodata[0]["lat"]
            record["longitude"] = geodata[0]["lon"]
            record["geoSource"] = "MapQuest"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: print sys.exc_info() # pass
    if geocodeFound: continue

#    print "No geoCode found for:", record["id"]

print count, " jobs processed in total."

# cleanup1: Remove companies without skills ? (they are geo-located! really delete?)
defectCount = scraperwiki.sqlite.select('count(*) FROM company_data5 WHERE skills = NULL OR skills = ""')[0]["count(*)"]
print "Starting to remove ", defectCount, " companies without skills!"
scraperwiki.sqlite.execute("DELETE FROM company_data5 WHERE skills = NULL OR skills = '';")
scraperwiki.sqlite.commit()

sys.exit()

# cleanup2: Remove duplicates
count = 0
jobCount  = scraperwiki.sqlite.select('count(*) FROM company_data5')[0]["count(*)"]
compCount = scraperwiki.sqlite.select('count(*) FROM (SELECT MAX(id) FROM company_data5 GROUP BY company, region)')[0]["count(*)"]
print "Starting to remove ", jobCount - compCount, " duplicates!"
scraperwiki.sqlite.execute("DELETE FROM company_data5 WHERE id NOT IN (SELECT MAX(id) FROM company_data5 GROUP BY company, region);")
scraperwiki.sqlite.commit()import scraperwiki
import sys
import urllib
from urllib import urlencode
import urllib2
from urlparse import urlparse
import json
import csv
import re
import simplejson
import time
from geopy.geocoders.base import Geocoder
from geopy.util import logger, decode_page, join_filter

scraperwiki.sqlite.attach("skillcheck_with_fixed_array")

# CHECK: Integrate duplicates (same company and region)
# TODO: Integrate data from company_data1-5 into company_data (rename company_data, create company_data, copy cd5, check rows from other company_data)
#scraperwiki.sqlite.execute("ALTER TABLE company_data RENAME TO company_data1")
#scraperwiki.sqlite.execute("ALTER TABLE company_data5 RENAME TO company_data")
#scraperwiki.sqlite.execute("drop table if exists company_data1")
#scraperwiki.sqlite.execute("drop table if exists company_data2")
#scraperwiki.sqlite.execute("drop table if exists company_data3")
#scraperwiki.sqlite.execute("drop table if exists company_data4")
#scraperwiki.sqlite.execute("drop table if exists company_data5")

# TODO: handle semantical duplicates ("Berlin" vs "Berlin, Germany") (by distance of geo-coord? using a file with cities (Berlin, New York, ...)?)
test = scraperwiki.sqlite.select("region FROM company_data5 WHERE region LIKE '%Berlin%' GROUP BY region")
print test
for row in test:
    print row

#scraperwiki.sqlite.execute("drop table if exists company_data5")
try:    scraperwiki.sqlite.execute("create table company_data5 (oldID, id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'company_data5' already exists."

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass

count = 0
#skip: companies  = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A")
companies = []
for record in companies:
    count = count + 1
    if count%1000 == 0: print count, " jobs processed."

    try:
        dataAlreadySaved = scraperwiki.sqlite.select("id from company_data5 where oldID='"+record["oldID"]+"'", verbose=0)
        if dataAlreadySaved: continue
    except: pass

    regionList = []
    regionText = record["region"]
    record["orginalRegion"] = record["region"]
    
    if regionText.endswith("USA") or regionText.endswith(", NY"):
        record["region"] = record["region"].replace("Us - Ca - ", "").replace("Usa-ca-", "")
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
        continue
    if "PLZ"          in regionText: continue
    if "Postleitzahl" in regionText: continue
    if "keine"        == regionText: continue

    if   regionText.count(',') >= 4: regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " und " in regionText:
        regionText = regionText.replace(" und ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " & " in regionText:
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " sowie " in regionText:
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " oder " in regionText:
        regionText = regionText.replace(" oder ",     ",")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " und/oder " in regionText:
        regionText = regionText.replace(" und/oder ", ",")
        regionList = regionText.split(',') 
    elif regionText.count(',') >= 1 and " and " in regionText:
        regionText = regionText.replace(" and ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" or ",     ",")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " or " in regionText:
        regionText = regionText.replace(" and ",      ",")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" or ",     ",")
        regionList = regionText.split(',')
    elif regionText.count(',') >= 1 and " and/or " in regionText:
        regionText = regionText.replace(" and/or ", ",")
        regionList = regionText.split(',') 
    elif regionText.count(',') >= 2 and "/" in regionText:
        regionList = regionText.split(',') 

    elif regionText.count('/') >= 2: 
        regionList = regionText.split('/')
        for fragment in regionList:
            if fragment.count('-') >= 2:
                regionList.extend(fragment.split('-'))
    elif regionText.count('/') >= 1 and " und " in regionText:
        regionText = regionText.replace(" und ",      "/")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     "/")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " oder " in regionText:
        regionText = regionText.replace(" und ",      "/")
        regionText = regionText.replace(" & ",        ",")
        regionText = regionText.replace(" sowie ",    ",")
        regionText = regionText.replace(" oder ",     "/")
        regionText = regionText.replace(" ODER ",     "/")
        regionText = regionText.replace(" bzw. ",     "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " und/oder " in regionText:
        regionText = regionText.replace(" und/oder ", "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " and " in regionText:
        regionText = regionText.replace(" and ",      "/")
        regionText = regionText.replace(" or ",       "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " or " in regionText:
        regionText = regionText.replace(" and ",      "/")
        regionText = regionText.replace(" or ",       "/")
        regionList = regionText.split('/')
    elif regionText.count('/') >= 1 and " and/or " in regionText:
        regionText = regionText.replace(" and/or ",   "/")
        regionList = regionText.split('/') 

#-
    elif regionText.count(';') >= 2: regionList = regionText.split(';')
    elif "\u2022" in regionText:     regionList = regionText.split('\u2022')
    elif "+" in regionText:          regionList = regionText.split('+')
    elif "+++" in regionText:        regionList = regionText.split('+++')
    elif " - " in regionText:        regionList = regionText.split(' - ')
    elif " oder " in regionText:     regionList = regionText.split(' oder ')
    elif " ODER " in regionText:     regionList = regionText.split(' ODER ')
    elif " bzw. " in regionText:     regionList = regionText.split(' bzw. ')
    elif " und " in regionText:      regionList = regionText.split(' und ')
    elif " UND " in regionText:      regionList = regionText.split(' UND ')
    elif " & " in regionText:        regionList = regionText.split(' & ')
    elif " sowie " in regionText:    regionList = regionText.split(' sowie ')
    elif " und/oder " in regionText: regionList = regionText.split(' und/oder ')
    elif " and " in regionText:      regionList = regionText.split(' and ')
    elif " or " in regionText:       regionList = regionText.split(' or ')
    elif " and/or " in regionText:   regionList = regionText.split(' and/or ')
    else:
        regionText = " ".join(regionText.strip().split())
        if   regionText.count(' ') >= 6: regionList = regionText.split(' ') #3
        elif regionText.count(',') >= 3: regionList = regionText.split(',')

    if regionList != []:
        regionList = list(set(regionList))
        record["oldID"] = record["id"]
#        print regionList, regionText
    else:
        for phrase in redundantText:
            record["region"] = record["region"].replace(phrase, " ")
        regionName = record["region"].strip()
        regionName = " ".join(regionName.split())
        regionName = regionName[:-1]  if regionName.endswith(',')   else regionName
        regionName = regionName[:-1]  if regionName.endswith('.')   else regionName
        regionName = regionName[1:-1] if regionName.startswith('(') and regionName.endswith(')')   else regionName
        regionName = regionName[:-1]  if regionName.endswith('(')   else regionName
        regionName = regionName[:-1]  if regionName.endswith(')')   and regionName.count("(") == 0    else regionName
#        regionName = regionName[1:]  if regionName.startswith('(') else regionName
        regionName = regionName[:-1]  if regionName.endswith('-')   else regionName
        regionName = regionName[1:]   if regionName.startswith('-') else regionName
        regionName = regionName.replace("( ","(").replace("/ ","/")
        if len(regionName) <= 2: continue
        regionName = " ".join(regionName.split())
        if regionName == "Esse":    regionName = "Essen"
        if len(regionName.replace("(","").replace(")","").replace("-","")) <= 2: continue
        record["region"]     = regionName
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
        continue

    regionCount = 1
    orgID = record["id"]
    for region in regionList:
        for phrase in redundantText:
            region = region.replace(phrase, " ")
        regionName = region.strip() #.replace("(","").replace(")","")
        regionName = " ".join(regionName.split())
        regionName = regionName[:-1] if regionName.endswith(',')   else regionName
        regionName = regionName[:-1] if regionName.endswith(',')   else regionName
        regionName = regionName[1:-1] if regionName.startswith('(') and regionName.endswith(')')   else regionName
        regionName = regionName[:-1] if regionName.endswith('(')   else regionName
        regionName = regionName[:-1] if regionName.endswith(')') and regionName.count("(") == 0    else regionName
#        regionName = regionName[1:]  if regionName.startswith('(') else regionName
        regionName = regionName[:-1] if regionName.endswith('-')   else regionName
        regionName = regionName[1:]  if regionName.startswith('-') else regionName
        regionName = regionName.replace("( ","(").replace("/ "," / ")
        regionName = " ".join(regionName.split())
        if len(regionName.replace("(","").replace(")","").replace("-","")) <= 2: continue
        if regionName == "oder":    continue
        if regionName == "von":     continue
        if regionName == "vor":     continue
        if regionName == "den":     continue
        if regionName == "mit":     continue
        if regionName == "f\u00fcr": continue
        if regionName == "für":     continue
        if regionName == "S\u00fcd": continue
        if regionName == "Augsbur": regionName = "Augsburg"
        if regionName == "Hambu":   regionName = "Hamburg"
        if regionName == "Esse":    regionName = "Essen"
        record["region"]     = regionName
        record["oldID"]      = orgID 
        scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)

#sys.exit()

mapquest_baseurl   = "http://open.mapquestapi.com/nominatim/v1/search?format=json&q="
googlemaps_baseurl = "http://maps.google.com/maps/api/geocode/json?sensor=false&address="
bingmaps_baseurl   = "http://dev.virtualearth.net/REST/v1/Locations?key=AiAuYPgWdmuTp4M5iPrPgw25Be4akjr2cWif56FDqM7mOVhSawBjMkoPoxop_wma&q="

#scraperwiki.sqlite.execute("drop table if exists company_data5")
try:    scraperwiki.sqlite.execute("create table company_data5 (id)")
except: print "Table 'company_data5' already exists."

#scraperwiki.sqlite.attach("skillcheck_with_fixed_array")
#companies  = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A WHERE NOT EXISTS(SELECT NULL FROM company_data5 AS B WHERE A.id=B.id)")
#companies = scraperwiki.sqlite.select("A.* FROM `skillcheck_with_fixed_array`.company_data AS A WHERE     EXISTS(SELECT NULL FROM company_data5 AS B WHERE A.id=B.id) ORDER BY A.company ASC")
companies  = scraperwiki.sqlite.select("* FROM company_data5 WHERE longitude = '' OR longitude IS NULL")
print "Total number of companies not geolocated:  ", len(companies)

# Start
count = 0
for record in companies:
#    if record["region"] == None: 
#        continue

    count = count + 1
    if count%1000 == 0: print count, " jobs processed."

    geocodeFound = False

    try: #check if geocode was already requested
        alreadyGeocoded = ""
        alreadyGeocoded = scraperwiki.sqlite.select("latitude, longitude FROM company_data5 WHERE region=? AND latitude IS NOT NULL LIMIT 1", (record["region"]), verbose=0)
        if alreadyGeocoded: 
            try:    record["latitude"]  = alreadyGeocoded[0]["latitude"]
            except: pass
            try:    record["longitude"] = alreadyGeocoded[0]["longitude"]
            except: pass
            try:    record["geoSource"] = alreadyGeocoded[0]["geoSource"]
            except: pass
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except:
        print sys.exc_info() # pass
    if geocodeFound: continue

    try: # ask google maps to geolocate
        geocode_url = googlemaps_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
            record["geoSource"] = "GoogleMaps"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: pass
    if geocodeFound: continue

    try: # ask bing maps to geolocate
        geocode_url = bingmaps_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]    = geodata["resourceSets"][0]["resources"][0]["point"]["coordinates"][0]
            record["longitude"]   = geodata["resourceSets"][0]["resources"][0]["point"]["coordinates"][1]
            record["geoSource"] = "BingMaps"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: pass
    if geocodeFound: continue

    try: # ask mapquest to geolocate
        geocode_url = mapquest_baseurl + urllib.quote(record["region"].replace(',','').encode('utf-8'))
#        geocode_url = mapquest_baseurl + urllib.quote_plus(urllib.quote(record["region"].encode('utf-8')))
        gmaps_req   = urllib2.Request(geocode_url)
        gmaps_res   = urllib2.urlopen(gmaps_req)
        geodata     = json.load(gmaps_res)#        geodata     = simplejson.loads(scraperwiki.scrape(geocode_url))
        if geodata != None and geodata != []:
            record["latitude"]  = geodata[0]["lat"]
            record["longitude"] = geodata[0]["lon"]
            record["geoSource"] = "MapQuest"
            scraperwiki.sqlite.save(["id"], data=record, table_name='company_data5', verbose=0)
            geocodeFound = True
    except: print sys.exc_info() # pass
    if geocodeFound: continue

#    print "No geoCode found for:", record["id"]

print count, " jobs processed in total."

# cleanup1: Remove companies without skills ? (they are geo-located! really delete?)
defectCount = scraperwiki.sqlite.select('count(*) FROM company_data5 WHERE skills = NULL OR skills = ""')[0]["count(*)"]
print "Starting to remove ", defectCount, " companies without skills!"
scraperwiki.sqlite.execute("DELETE FROM company_data5 WHERE skills = NULL OR skills = '';")
scraperwiki.sqlite.commit()

sys.exit()

# cleanup2: Remove duplicates
count = 0
jobCount  = scraperwiki.sqlite.select('count(*) FROM company_data5')[0]["count(*)"]
compCount = scraperwiki.sqlite.select('count(*) FROM (SELECT MAX(id) FROM company_data5 GROUP BY company, region)')[0]["count(*)"]
print "Starting to remove ", jobCount - compCount, " duplicates!"
scraperwiki.sqlite.execute("DELETE FROM company_data5 WHERE id NOT IN (SELECT MAX(id) FROM company_data5 GROUP BY company, region);")
scraperwiki.sqlite.commit()