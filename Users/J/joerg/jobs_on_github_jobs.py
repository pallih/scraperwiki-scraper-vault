import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html
import urllib
import urllib2
from urlparse import urlparse
import json
import csv
import time
import dateutil.parser
from datetime import datetime, date, time
import re

# List of text phrases to be removed from data
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))

def scrapeTable(root): 
    global countNew
    for job in root.cssselect(".positionlist tr"):
        record = {}

        jobName = job.cssselect(".title h4 a")
        try:    jobName[0]
        except: continue
        idString                          = jobName[0].attrib['href']
        index1                            = idString.rfind("/") + 1
        try:    idNumber                  = idString[index1:]
        except: idNumber                  = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]      = idNumber
        except: pass
        try:    record["name"]    = " ".join(jobName[0].text.strip().split())
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect(".meta .when")[0].text)
        except: pass
        record["region"]          = ""
        try:
            record["region"]      = job.cssselect(".meta .location")[0].text.strip()
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]      = re.sub("^- ", "", record["region"]).strip()
            record["region"]      = re.sub("^, ", "", record["region"]).strip()
            record["region"]      = " ".join(record["region"].replace("SF /","San Francisco, CA, USA").split())
        except: pass

        try:
            record["company"]     = " ".join(job.cssselect(".title .source .company")[0].text.strip().split())
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
        except: pass

        try:
            pageHTML                   = scraperwiki.scrape("https://jobs.github.com"+jobName[0].attrib['href'])
            pageRoot                   = lxml.html.fromstring(pageHTML)
            try: record["description"] = " ".join(pageRoot.cssselect(".column.main")[0].text_content().strip().split())
            except: pass
            try: record["companyURL"]  = "http://" + urlparse(pageRoot.cssselect(".column.sidebar .logo .url a")[0].attrib['href']).hostname
            except: pass
            try: record["logoURL"]     = "http:" + pageRoot.cssselect(".column.sidebar .logo .logo img")[0].attrib['src']
            except: pass
        except: pass

        scraperwiki.sqlite.save(["id"], record)        
        countNew = countNew + 1

        regionList = []
        regionText = record["region"]
        if   regionText.count('.') >= 1: regionList = regionText.split('.')
        elif regionText.count(',') >= 3: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 1: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        if regionList != []:
            regionList = list(set(regionList))
#            print regionList, regionText
        
        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            regionName = region.strip()
            if len(regionName) <= 2: continue
            record["region"]     = regionName
            record["id"]         = orgID + "_" + str(regionCount)
            regionCount          = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
            countNew = countNew + 1

#start
countNew = 0
maxPages = 10 # max is 263 jobs (50 per page)
baseURL  = "https://jobs.github.com/positions?page="

#scraperwiki.sqlite.execute("ALTER TABLE swdata RENAME TO swdata_old;")

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    sUrl  = baseURL + str(page)
    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

sys.exit()

#cleanup
rows = scraperwiki.sqlite.select("* FROM swdata ORDER BY LENGTH(region) DESC")
print "Starting cleanup of ", len(rows), " rows!"
for record in rows:
    try:    
        for phrase in redundantText:
            record["company"]  = record["company"].replace(phrase, " ").strip()
    except: pass
    try:    
        for phrase in redundantText:
            record["name"]  = record["name"].replace(phrase, " ").strip()
    except: pass
    try:    
        record["region"]      = record["region"]
        for phrase in redundantText:
            record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            record["region"]      = " ".join(record["region"].split())
        scraperwiki.sqlite.save(["id"], record)

        regionList = []
        regionText = record["region"]
        if   regionText.count('.') >= 1: regionList = regionText.split('.')
        elif regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 1: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        if regionList != []:
            regionList = list(set(regionList))
#            print regionList, regionText

        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            regionName = region.strip()
            if len(regionName) <= 2: continue
            record["region"] = regionName
            record["id"]     = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
    except: pass


import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html
import urllib
import urllib2
from urlparse import urlparse
import json
import csv
import time
import dateutil.parser
from datetime import datetime, date, time
import re

# List of text phrases to be removed from data
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))

def scrapeTable(root): 
    global countNew
    for job in root.cssselect(".positionlist tr"):
        record = {}

        jobName = job.cssselect(".title h4 a")
        try:    jobName[0]
        except: continue
        idString                          = jobName[0].attrib['href']
        index1                            = idString.rfind("/") + 1
        try:    idNumber                  = idString[index1:]
        except: idNumber                  = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]      = idNumber
        except: pass
        try:    record["name"]    = " ".join(jobName[0].text.strip().split())
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect(".meta .when")[0].text)
        except: pass
        record["region"]          = ""
        try:
            record["region"]      = job.cssselect(".meta .location")[0].text.strip()
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]      = re.sub("^- ", "", record["region"]).strip()
            record["region"]      = re.sub("^, ", "", record["region"]).strip()
            record["region"]      = " ".join(record["region"].replace("SF /","San Francisco, CA, USA").split())
        except: pass

        try:
            record["company"]     = " ".join(job.cssselect(".title .source .company")[0].text.strip().split())
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
        except: pass

        try:
            pageHTML                   = scraperwiki.scrape("https://jobs.github.com"+jobName[0].attrib['href'])
            pageRoot                   = lxml.html.fromstring(pageHTML)
            try: record["description"] = " ".join(pageRoot.cssselect(".column.main")[0].text_content().strip().split())
            except: pass
            try: record["companyURL"]  = "http://" + urlparse(pageRoot.cssselect(".column.sidebar .logo .url a")[0].attrib['href']).hostname
            except: pass
            try: record["logoURL"]     = "http:" + pageRoot.cssselect(".column.sidebar .logo .logo img")[0].attrib['src']
            except: pass
        except: pass

        scraperwiki.sqlite.save(["id"], record)        
        countNew = countNew + 1

        regionList = []
        regionText = record["region"]
        if   regionText.count('.') >= 1: regionList = regionText.split('.')
        elif regionText.count(',') >= 3: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 1: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        if regionList != []:
            regionList = list(set(regionList))
#            print regionList, regionText
        
        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            regionName = region.strip()
            if len(regionName) <= 2: continue
            record["region"]     = regionName
            record["id"]         = orgID + "_" + str(regionCount)
            regionCount          = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
            countNew = countNew + 1

#start
countNew = 0
maxPages = 10 # max is 263 jobs (50 per page)
baseURL  = "https://jobs.github.com/positions?page="

#scraperwiki.sqlite.execute("ALTER TABLE swdata RENAME TO swdata_old;")

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    sUrl  = baseURL + str(page)
    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

sys.exit()

#cleanup
rows = scraperwiki.sqlite.select("* FROM swdata ORDER BY LENGTH(region) DESC")
print "Starting cleanup of ", len(rows), " rows!"
for record in rows:
    try:    
        for phrase in redundantText:
            record["company"]  = record["company"].replace(phrase, " ").strip()
    except: pass
    try:    
        for phrase in redundantText:
            record["name"]  = record["name"].replace(phrase, " ").strip()
    except: pass
    try:    
        record["region"]      = record["region"]
        for phrase in redundantText:
            record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            record["region"]      = " ".join(record["region"].split())
        scraperwiki.sqlite.save(["id"], record)

        regionList = []
        regionText = record["region"]
        if   regionText.count('.') >= 1: regionList = regionText.split('.')
        elif regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 1: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        if regionList != []:
            regionList = list(set(regionList))
#            print regionList, regionText

        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            regionName = region.strip()
            if len(regionName) <= 2: continue
            record["region"] = regionName
            record["id"]     = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
    except: pass


