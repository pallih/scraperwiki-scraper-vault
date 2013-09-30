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
#import time
import dateutil.parser
from datetime import datetime, date, time, timedelta

google_maps_baseurl = "http://maps.google.com/maps/api/geocode/json?address="

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdGZFNkVZZTRtQzlMSThzUjQ1LU9VTXc&range=A2%3AA2000&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))
today = datetime.now() #datetime.datetime.now()

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
    for job in root.cssselect("div[itemtype*=JobPosting]"):
        record  = {}
        jobName = job.cssselect(".lead a[itemprop~=url]")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib['href']
        index1                        = idString.rfind("/") + 1
        try:    idNumber              = idString[index1:idString.find("-")]
        except: idNumber              = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]                  = idNumber
        record["name"]                = " ".join(jobName[0].text_content().strip().split())
        record["tags"]                = []

        regionList  = []
        locList = job.cssselect("a[href*=location]")
        record['originalRegion']      = locList
        for loc in locList:
            region = loc.text_content().strip()
            for phrase in redundantText:
                region = " ".join(region.split()).replace(phrase, " ").strip()
            regionList.append(" ".join(region.split()).replace(";", "").strip())
        regionList                    = list(set(regionList))

        try:    record["date"]        = dateutil.parser.parse(job.cssselect("span.pull-right")[0].text.strip())
        except: record["date"]        = job.cssselect("span.pull-right")[0].text.strip()
        try:    record["company"]     = " ".join(job.cssselect("strong")[0].text.strip().split())
        except: pass

        record["country"]             = ""
        try:
            pageHTML                  = scraperwiki.scrape("http://findgrailsjobs.com"+jobName[0].attrib['href'])
            pageRoot                  = lxml.html.fromstring(pageHTML)
            record["description"]     = " ".join(pageRoot.cssselect("div[itemtype*=JobPosting]")[0].text_content().strip().split())
            try:    record["logoURL"] = pageRoot.cssselect("div[itemtype*=JobPosting] .pull-right   img")[0].attrib['src']
            except: record["logoURL"] = pageRoot.cssselect("div[itemtype*=JobPosting] .company-logo img")[0].attrib['src']
#            record["companyURL"]      = pageRoot.cssselect(".post-content a[href!=mailto]")[0].attrib['href']
        except: print sys.exc_info() # pass

        #save in datastore
        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            record["region"] = region
            if regionCount == 1: record["id"] = orgID
            else:                record["id"] = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 5
baseURL  = "http://findgrailsjobs.com/?max=25&offset="

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page
    sUrl  = baseURL + str(page * 25)
    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

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
#import time
import dateutil.parser
from datetime import datetime, date, time, timedelta

google_maps_baseurl = "http://maps.google.com/maps/api/geocode/json?address="

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdGZFNkVZZTRtQzlMSThzUjQ1LU9VTXc&range=A2%3AA2000&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))
today = datetime.now() #datetime.datetime.now()

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
    for job in root.cssselect("div[itemtype*=JobPosting]"):
        record  = {}
        jobName = job.cssselect(".lead a[itemprop~=url]")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib['href']
        index1                        = idString.rfind("/") + 1
        try:    idNumber              = idString[index1:idString.find("-")]
        except: idNumber              = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]                  = idNumber
        record["name"]                = " ".join(jobName[0].text_content().strip().split())
        record["tags"]                = []

        regionList  = []
        locList = job.cssselect("a[href*=location]")
        record['originalRegion']      = locList
        for loc in locList:
            region = loc.text_content().strip()
            for phrase in redundantText:
                region = " ".join(region.split()).replace(phrase, " ").strip()
            regionList.append(" ".join(region.split()).replace(";", "").strip())
        regionList                    = list(set(regionList))

        try:    record["date"]        = dateutil.parser.parse(job.cssselect("span.pull-right")[0].text.strip())
        except: record["date"]        = job.cssselect("span.pull-right")[0].text.strip()
        try:    record["company"]     = " ".join(job.cssselect("strong")[0].text.strip().split())
        except: pass

        record["country"]             = ""
        try:
            pageHTML                  = scraperwiki.scrape("http://findgrailsjobs.com"+jobName[0].attrib['href'])
            pageRoot                  = lxml.html.fromstring(pageHTML)
            record["description"]     = " ".join(pageRoot.cssselect("div[itemtype*=JobPosting]")[0].text_content().strip().split())
            try:    record["logoURL"] = pageRoot.cssselect("div[itemtype*=JobPosting] .pull-right   img")[0].attrib['src']
            except: record["logoURL"] = pageRoot.cssselect("div[itemtype*=JobPosting] .company-logo img")[0].attrib['src']
#            record["companyURL"]      = pageRoot.cssselect(".post-content a[href!=mailto]")[0].attrib['href']
        except: print sys.exc_info() # pass

        #save in datastore
        regionCount = 1
        orgID = record["id"]
        for region in regionList:
            record["region"] = region
            if regionCount == 1: record["id"] = orgID
            else:                record["id"] = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 5
baseURL  = "http://findgrailsjobs.com/?max=25&offset="

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page
    sUrl  = baseURL + str(page * 25)
    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

