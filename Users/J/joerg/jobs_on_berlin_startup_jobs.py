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
    for job in root.cssselect(".list .post"):
        record = {}       
        jobName = job.cssselect("h2 a")
        try:    jobName[0]
        except: jobName = []

        idString         = job.attrib['id']
        index1           = idString.rfind("_") + 1
        try:    idNumber = idString[index1:]
        except: idNumber = idString

#        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
#        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["name"]            = " ".join(jobName[0].text.strip().split())
        record["tags"]            = []
        try:
            linkList = job.cssselect(".post-category a")
            for link in linkList: 
                if link.attrib['href'].find("companies") >= 0 : record["company"] = link.text
                else: record["tags"].append(link.text)
        except: pass

        try:
            record["date"]    = dateutil.parser.parse(job.cssselect(".post-date")[0].text)
        except: print sys.exc_info() #pass

        record["region"]          = "Berlin, Germany"
        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["description"] = " ".join(lxml.html.fromstring(clean_html(pageHTML)).text_content().split())
#            record["logoURL"]     = pageRoot.cssselect(".meta-jobs-img")[0].attrib['src']
#            record["companyURL"]  = pageRoot.cssselect(".post-content a[href!=mailto]")[0].attrib['href']
            try:
                linkList = pageRoot.cssselect(".post-content a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") < 1: record["companyURL"] = "http://" + str(urlparse(link.attrib['href']).hostname)
            except: print sys.exc_info() # pass
            try:
                tagList = pageRoot.cssselect(".post-footer a[rel=tag]")
                for tag in tagList: record["tags"].append(" ".join(tag.text.strip().split())) 
            except: pass
        except: print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
#        scraperwiki.sqlite.save(["id"], record)
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 20 #15
baseURL  = "http://berlinstartupjobs.com/page/"

scraperwiki.sqlite.execute("drop table if exists swdata2")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    print sUrl

    try:
        html  = scraperwiki.scrape(sUrl)
        root  = lxml.html.fromstring(html)
        scrapeTable(root)
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
#import time
import dateutil.parser
from datetime import datetime, date, time, timedelta

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
    for job in root.cssselect(".list .post"):
        record = {}       
        jobName = job.cssselect("h2 a")
        try:    jobName[0]
        except: jobName = []

        idString         = job.attrib['id']
        index1           = idString.rfind("_") + 1
        try:    idNumber = idString[index1:]
        except: idNumber = idString

#        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
#        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["name"]            = " ".join(jobName[0].text.strip().split())
        record["tags"]            = []
        try:
            linkList = job.cssselect(".post-category a")
            for link in linkList: 
                if link.attrib['href'].find("companies") >= 0 : record["company"] = link.text
                else: record["tags"].append(link.text)
        except: pass

        try:
            record["date"]    = dateutil.parser.parse(job.cssselect(".post-date")[0].text)
        except: print sys.exc_info() #pass

        record["region"]          = "Berlin, Germany"
        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["description"] = " ".join(lxml.html.fromstring(clean_html(pageHTML)).text_content().split())
#            record["logoURL"]     = pageRoot.cssselect(".meta-jobs-img")[0].attrib['src']
#            record["companyURL"]  = pageRoot.cssselect(".post-content a[href!=mailto]")[0].attrib['href']
            try:
                linkList = pageRoot.cssselect(".post-content a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") < 1: record["companyURL"] = "http://" + str(urlparse(link.attrib['href']).hostname)
            except: print sys.exc_info() # pass
            try:
                tagList = pageRoot.cssselect(".post-footer a[rel=tag]")
                for tag in tagList: record["tags"].append(" ".join(tag.text.strip().split())) 
            except: pass
        except: print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
#        scraperwiki.sqlite.save(["id"], record)
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 20 #15
baseURL  = "http://berlinstartupjobs.com/page/"

scraperwiki.sqlite.execute("drop table if exists swdata2")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    print sUrl

    try:
        html  = scraperwiki.scrape(sUrl)
        root  = lxml.html.fromstring(html)
        scrapeTable(root)
    except: pass
