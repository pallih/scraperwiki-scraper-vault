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
    for job in root.cssselect("div.job"):
        record = {}

        idNumber                      = job.attrib['data-jobid']

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["company"]         = " ".join(job.cssselect(".employer")[0].text.strip().split())
        regionText                = " ".join(job.cssselect(".location")[0].text.strip().split())
        record['originalRegion']  = regionText
        for phrase in redundantText:
            regionText = regionText.replace(phrase, " ").strip()
        regionList = regionText.split(';')

        jobName = job.cssselect("a.title")
        record["name"]               = " ".join(jobName[0].text.strip().split())
        pageHTML                     = scraperwiki.scrape("http://careers.stackoverflow.com"+jobName[0].attrib['href'])
        pageRoot                     = lxml.html.fromstring(pageHTML)
        record["description"]        = " ".join(pageRoot.cssselect("div.jobdetail")[0].text_content().strip().split())
        try:    record["logoURL"]    = pageRoot.cssselect("div#companylogo img")[0].attrib['src']
        except: pass
        try:    record["companyURL"] = "http://" + urlparse(pageRoot.cssselect("a.employer")[0].attrib['href']).hostname
        except: pass

        record["country"]            = ""       #TODO: parse region(s)?
        record["date"]               = today    #Not exact but at least an approximative date
        record["tags"]               = []
        for tag in job.cssselect(".post-tag"):
            record["tags"].append(" ".join(tag.text.strip().split()))

        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            record["region"] = region
            if regionCount == 1: record["id"] = orgID
            else:                record["id"] = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

#start
maxPages = 50 # max is mostly 33
baseURL  = "http://careers.stackoverflow.com/jobs?pg="
today = datetime.now()

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
#    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    try:
        currentPage = int(root.cssselect(".pagination a.selected")[0].text.strip())
        if page != currentPage: break
    except:
        print "Last page with job list was: ", page
        break
    scrapeTable(root)

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
    scraperwiki.sqlite.save(["id"], record)import scraperwiki
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
    for job in root.cssselect("div.job"):
        record = {}

        idNumber                      = job.attrib['data-jobid']

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["company"]         = " ".join(job.cssselect(".employer")[0].text.strip().split())
        regionText                = " ".join(job.cssselect(".location")[0].text.strip().split())
        record['originalRegion']  = regionText
        for phrase in redundantText:
            regionText = regionText.replace(phrase, " ").strip()
        regionList = regionText.split(';')

        jobName = job.cssselect("a.title")
        record["name"]               = " ".join(jobName[0].text.strip().split())
        pageHTML                     = scraperwiki.scrape("http://careers.stackoverflow.com"+jobName[0].attrib['href'])
        pageRoot                     = lxml.html.fromstring(pageHTML)
        record["description"]        = " ".join(pageRoot.cssselect("div.jobdetail")[0].text_content().strip().split())
        try:    record["logoURL"]    = pageRoot.cssselect("div#companylogo img")[0].attrib['src']
        except: pass
        try:    record["companyURL"] = "http://" + urlparse(pageRoot.cssselect("a.employer")[0].attrib['href']).hostname
        except: pass

        record["country"]            = ""       #TODO: parse region(s)?
        record["date"]               = today    #Not exact but at least an approximative date
        record["tags"]               = []
        for tag in job.cssselect(".post-tag"):
            record["tags"].append(" ".join(tag.text.strip().split()))

        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            record["region"] = region
            if regionCount == 1: record["id"] = orgID
            else:                record["id"] = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

#start
maxPages = 50 # max is mostly 33
baseURL  = "http://careers.stackoverflow.com/jobs?pg="
today = datetime.now()

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
#    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    try:
        currentPage = int(root.cssselect(".pagination a.selected")[0].text.strip())
        if page != currentPage: break
    except:
        print "Last page with job list was: ", page
        break
    scrapeTable(root)

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