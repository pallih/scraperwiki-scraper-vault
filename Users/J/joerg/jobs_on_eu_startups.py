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
    for job in root.cssselect("table#wpjb_jobboard tbody tr"):
        record = {}       
        try: jobName = job.cssselect("td")[1].cssselect("a")
        except: continue
        try:    jobName[0]
        except: jobName = []

        idNumber              = jobName[0].attrib["href"][jobName[0].attrib["href"].rfind("/")+1:]

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]          = idNumber
        except: pass
        try:    record["name"]        = " ".join(job.cssselect("td")[1].cssselect("a")[0].text.strip().split())
        except: pass
        try:    record["tags"]        = ["Startup"]
        except: pass
        try:
            record["region"]          = " ".join(job.cssselect("td")[2].text.replace("/","").replace("+","").strip().split())
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]      = record["region"].replace(phrase, " ").strip()
        except: pass
        try:    record["date"]        = dateutil.parser.parse(job.cssselect("td")[0].text.strip())
        except: pass
#        record["country"]             = ""

#        try:
#            gmaps_url = "%s%s&sensor=false" % (google_maps_baseurl, urllib.quote_plus(urllib.quote(record["region"])))
#            response = urllib2.urlopen(gmaps_url)
#            geodata = json.load(response)
#            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
#            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
#        except: print sys.exc_info()[0] # pass

        try:
            pageHTML                  = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot                  = lxml.html.fromstring(pageHTML)
            record["description"]     = " ".join(pageRoot.cssselect(".wpjb_job_content")[0].text_content().strip().split())
            record["companyURL"]      = pageRoot.cssselect(".wpjb_job_info tbody tr")[0].cssselect("td")[1].cssselect("a")[0].attrib['href']
            try:    
                record["company"] = pageRoot.cssselect(".wpjb_job_info tbody tr")[0].cssselect("td")[1].cssselect("a")[0].text
            except: pass
            try:    
                record["logoURL"] = pageRoot.cssselect(".wpjb_job_text img")[0].attrib['src']
            except: pass
        except: print sys.exc_info()[0] # pass

        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

# start: initialize variables
maxPages = 10
baseURL  = "http://www.eu-startups.com/startup-jobs/page/"

#scraperwiki.sqlite.execute("ALTER TABLE swdata RENAME TO swdata_old;")

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
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
    for job in root.cssselect("table#wpjb_jobboard tbody tr"):
        record = {}       
        try: jobName = job.cssselect("td")[1].cssselect("a")
        except: continue
        try:    jobName[0]
        except: jobName = []

        idNumber              = jobName[0].attrib["href"][jobName[0].attrib["href"].rfind("/")+1:]

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]          = idNumber
        except: pass
        try:    record["name"]        = " ".join(job.cssselect("td")[1].cssselect("a")[0].text.strip().split())
        except: pass
        try:    record["tags"]        = ["Startup"]
        except: pass
        try:
            record["region"]          = " ".join(job.cssselect("td")[2].text.replace("/","").replace("+","").strip().split())
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]      = record["region"].replace(phrase, " ").strip()
        except: pass
        try:    record["date"]        = dateutil.parser.parse(job.cssselect("td")[0].text.strip())
        except: pass
#        record["country"]             = ""

#        try:
#            gmaps_url = "%s%s&sensor=false" % (google_maps_baseurl, urllib.quote_plus(urllib.quote(record["region"])))
#            response = urllib2.urlopen(gmaps_url)
#            geodata = json.load(response)
#            record["latitude"]    = geodata["results"][0]["geometry"]["location"]["lat"]
#            record["longitude"]   = geodata["results"][0]["geometry"]["location"]["lng"]
#        except: print sys.exc_info()[0] # pass

        try:
            pageHTML                  = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot                  = lxml.html.fromstring(pageHTML)
            record["description"]     = " ".join(pageRoot.cssselect(".wpjb_job_content")[0].text_content().strip().split())
            record["companyURL"]      = pageRoot.cssselect(".wpjb_job_info tbody tr")[0].cssselect("td")[1].cssselect("a")[0].attrib['href']
            try:    
                record["company"] = pageRoot.cssselect(".wpjb_job_info tbody tr")[0].cssselect("td")[1].cssselect("a")[0].text
            except: pass
            try:    
                record["logoURL"] = pageRoot.cssselect(".wpjb_job_text img")[0].attrib['src']
            except: pass
        except: print sys.exc_info()[0] # pass

        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

# start: initialize variables
maxPages = 10
baseURL  = "http://www.eu-startups.com/startup-jobs/page/"

#scraperwiki.sqlite.execute("ALTER TABLE swdata RENAME TO swdata_old;")

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)

