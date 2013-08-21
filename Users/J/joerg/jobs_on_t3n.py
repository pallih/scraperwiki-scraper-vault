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

def fix_encoding_mistakes(unistr):
    import itertools
    l = [(0b11000010, i) for i in range(0b10100000, 0b10111111 + 1)]
    l += [(0b11000011, i) for i in range(0b10000000, 0b10111111 + 1)]
    for a, b in l:
        l1_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin1')
        l9_mistake = ('%s%s' % (chr(a), chr(b))).decode('latin9')
        l1_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8')
        unistr = unistr.replace(l1_mistake, l1_fix)
        if l9_mistake != l1_mistake:
            l9_fix = ('%s%s' % (chr(a), chr(b))).decode('utf-8').encode('latin1').decode('latin9')
            unistr = unistr.replace(l9_mistake, l9_fix)
    unistr = unistr.replace(u'\xe2\x82\xac', u'\u20ac')
    return unistr

def scrapeTable(root): 
    global countNew
    for job in root.cssselect("#job-posts li"):
        record = {}

        jobName = job.cssselect("a .thingTitle h2")
        try:    jobName[0]
        except: continue
        idString                          = job.cssselect("a")[0].attrib['href']

#        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'")
#        if dataAlreadySaved: continue

        try:    record["id"]      = idString
        except: pass
        try:    record["name"]    = " ".join(jobName[0].text.strip().split())
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect("a .thingMeta")[0].text)
        except: pass
        record["region"]          = ""
        try:    
#            print job.cssselect(".thingDescr")[0].text_content()
            record["region"]      = fix_encoding_mistakes(" ".join(job.cssselect("a .thingDescr")[0].text_content().strip().split()))
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
        except: print sys.exc_info() #pass

        try:
            record["company"]     = " ".join(job.cssselect("a .thingTitle h3")[0].text.strip().split())
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
        except: pass

        try:
            pageHTML                   = scraperwiki.scrape(job.cssselect("a")[0].attrib['href'])
            pageRoot                   = lxml.html.fromstring(pageHTML)
            try: record["description"] = " ".join(pageRoot.cssselect(".jobSingleView")[0].text_content().strip().split())
            except: record["description"] = " ".join(pageRoot.cssselect("body")[0].text_content().strip().split())
            try: record["companyURL"]  = "http://" + urlparse(pageRoot.cssselect(".contentInnerShadow .cf .col50 a")[0].attrib['href']).hostname
            except: pass
            try: record["logoURL"]     = pageRoot.cssselect(".contentInnerShadow .cf .col30 img")[0].attrib['src']
            except: pass
            try: record["contactInfo"]     = " ".join(pageRoot.cssselect("#job-details .cf .col50 .cBox")[0].text_content().strip().split())
            except: pass
        except: pass

        scraperwiki.sqlite.save(["id"], record)        
        countNew = countNew + 1

        regionList = []
        regionText = record["region"]
        if   regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 1: regionList = regionText.split('/')
        elif regionText.count(';') >= 2: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
#        elif "/" in regionText:          regionList = regionText.split('/')
#        elif "-" in regionText:          regionList = regionText.split('-')
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
maxPages = 7 # max is 263 jobs (50 per page)
baseURL  = "http://t3n.de/jobs/home/"

#scraperwiki.sqlite.execute("drop table if exists swdata")
#try:    scraperwiki.sqlite.execute("create table swdata (id)")
#except: print "Table 'swdata' probably already exists."

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
            record["region"]  = record["region"].replace(phrase, " ").strip()
    except: pass
    try:    
        for phrase in redundantText:
            record["name"]  = record["name"].replace(phrase, " ").strip()
    except: pass
    scraperwiki.sqlite.save(["id"], record)