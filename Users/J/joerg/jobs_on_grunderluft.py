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

#google_maps_baseurl = "http://maps.google.com/maps/api/geocode/json?address="

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
    for job in root.cssselect("#main_left table tr"):
        record = {}       
        jobName = job.cssselect(".title a")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib["href"]
        index1                        = idString.rfind("/") + 1
        try:    idNumber              = idString[index1:]
        except: idNumber              = idString

#        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
#        if dataAlreadySaved: continue

        try:    record["id"]              = idNumber
        except: pass
        try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
        except: pass
        try:    record["tags"]            = []
        except: pass
        try:    record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect(".company")[0].text.strip().split()))
        except: pass
        try:    record["region"]          = fix_encoding_mistakes(" ".join(job.cssselect(".location")[0].text.strip().split())) + ", Deutschland"
        except: pass
        try:    record["originalRegion"]  = fix_encoding_mistakes(" ".join(job.cssselect(".location")[0].text.strip().split()))
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect(".created_at")[0].text + " 2013")
        except: pass

        try:
            logoURL                   = job.cssselect(".ad_logo")[0].get('style')
            index1                    = logoURL.find("'") + 1
            index2                    = logoURL.rfind("'")
            record["logoURL"]         = "http://www.gruenderluft.de"+logoURL[index1:index2]
        except: pass

#        try:
#            gmaps_url = "%s%s&sensor=false" % (google_maps_baseurl, urllib.quote_plus(urllib.quote(record["region"])))
#            response = urllib2.urlopen(gmaps_url)
#            geodata = json.load(response)
#            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
#            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
#        except: print sys.exc_info()[0] # pass
        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape("http://www.gruenderluft.de" + jobName[0].attrib['href'])
            pageRoot              = c
            try:
                linkList = pageRoot.cssselect(".main_left a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") == -1 : record["companyURL"] = "http://" + urlparse(link.attrib['href']).hostname
            except: pass
            # TODO: parse description from PDF via Embedded Flash
            try:    record["description"] = " ".join(pageRoot.cssselect(".main_left")[0].text_content().strip().split())
            except: record["description"] = lxml.html.fromstring(clean_html(pageHTML)).text_content().strip()
        except: pass #print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

# start: initialize variables
maxPages = 20
baseURL  = "http://www.gruenderluft.de/page/"

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    #print sUrl

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

#google_maps_baseurl = "http://maps.google.com/maps/api/geocode/json?address="

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
    for job in root.cssselect("#main_left table tr"):
        record = {}       
        jobName = job.cssselect(".title a")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib["href"]
        index1                        = idString.rfind("/") + 1
        try:    idNumber              = idString[index1:]
        except: idNumber              = idString

#        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
#        if dataAlreadySaved: continue

        try:    record["id"]              = idNumber
        except: pass
        try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
        except: pass
        try:    record["tags"]            = []
        except: pass
        try:    record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect(".company")[0].text.strip().split()))
        except: pass
        try:    record["region"]          = fix_encoding_mistakes(" ".join(job.cssselect(".location")[0].text.strip().split())) + ", Deutschland"
        except: pass
        try:    record["originalRegion"]  = fix_encoding_mistakes(" ".join(job.cssselect(".location")[0].text.strip().split()))
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect(".created_at")[0].text + " 2013")
        except: pass

        try:
            logoURL                   = job.cssselect(".ad_logo")[0].get('style')
            index1                    = logoURL.find("'") + 1
            index2                    = logoURL.rfind("'")
            record["logoURL"]         = "http://www.gruenderluft.de"+logoURL[index1:index2]
        except: pass

#        try:
#            gmaps_url = "%s%s&sensor=false" % (google_maps_baseurl, urllib.quote_plus(urllib.quote(record["region"])))
#            response = urllib2.urlopen(gmaps_url)
#            geodata = json.load(response)
#            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
#            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
#        except: print sys.exc_info()[0] # pass
        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape("http://www.gruenderluft.de" + jobName[0].attrib['href'])
            pageRoot              = c
            try:
                linkList = pageRoot.cssselect(".main_left a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") == -1 : record["companyURL"] = "http://" + urlparse(link.attrib['href']).hostname
            except: pass
            # TODO: parse description from PDF via Embedded Flash
            try:    record["description"] = " ".join(pageRoot.cssselect(".main_left")[0].text_content().strip().split())
            except: record["description"] = lxml.html.fromstring(clean_html(pageHTML)).text_content().strip()
        except: pass #print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

# start: initialize variables
maxPages = 20
baseURL  = "http://www.gruenderluft.de/page/"

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    #print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

