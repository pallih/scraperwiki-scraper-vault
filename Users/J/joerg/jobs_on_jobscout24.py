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
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
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
    for job in root.cssselect(".jobList_table tr td"):
        record  = {}       
        jobName = job.cssselect("a.joblisteJobtitel")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib['href']
        index1                        = idString.rfind("=") + 1
        try:    idNumber              = idString[index1:]
        except: idNumber              = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]              = idNumber
        except: pass
        try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
        except: pass
        try:    record["tags"]            = []
        except: pass
        try:    record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect(".joblisteFirma")[0].text.strip().split()))
        except: pass
        regionText = ""
        try:    
            record["region"]          = fix_encoding_mistakes(" ".join(job.cssselect(".joblisteEinsatzorte")[0].text.strip().split())) + ", Deutschland"
            record['originalRegion']  = record['region']
            regionText = record["region"]
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass
        try:
            dateString                    = " ".join(job.cssselect("#PostedDate")[0].text.strip().split())
            if   dateString.find("Stunde") >= 0 or dateString.find("Minute") >= 0:
                record["date"]                = today
            elif dateString.find("Tag") >= 0:
                record["date"]                = dateutil.parser.parse(job.cssselect(".created_at")[0].text + "2013")
            else:
                dateOffset        = int(job.cssselect("p")[0].text.replace("Online seit","").replace("Tagen","").replace("Tag","").strip())
                record["date"] = today - timedelta(days=dateOffset)                
        except: pass
        try:    record["logoURL"]         = job.cssselect(".joblisteBodyLogo img")[0].attrib['src']
        except: pass

        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(pageHTML)
            try:
                linkList = pageRoot.cssselect("#job_detail a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") == -1 : record["companyURL"] = "http://" + urlparse(link.attrib['href']).hostname
            except: pass
            record["description"] = " ".join(pageRoot.cssselect("#job_detail")[0].text_content().strip().split())
        except: print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

        regionList = []
        if   regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
#        if "/" in regionText:            regionList = regionText.split('/')
        elif regionText.count(';') >= 2: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
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
            record["region"] = regionName
            record["id"]     = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
            countNew = countNew + 1

# start: initialize variables
maxPages = 200
#baseURL  = "http://www.jobscout24.de/Jobs_Ergebnisliste.html?pg="
baseURL  = "http://www.jobscout24.de/Jobs_Ergebnisliste.html?exCrit=%3bNVJTL%3dJN008&pg="

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    #print sUrl

    try:
        html  = scraperwiki.scrape(sUrl)
        root  = lxml.html.fromstring(html)
        scrapeTable(root)
    except: sys.exc_info()

#sys.exit()

#cleanup
count = 0
jobCount = scraperwiki.sqlite.select('count(*) FROM swdata')[0]["count(*)"]
print "Starting cleanup of ", jobCount, " rows!"
windowLength = 500
windowCount  = jobCount / windowLength
offset       = scraperwiki.sqlite.get_var("offset", 0)
for window in range(windowCount):
    rows = scraperwiki.sqlite.select('* from swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset) )
    for record in rows:
        count = count + 1
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+ offset
        try:  
            record["company"] = fix_encoding_mistakes(record["company"])
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]      = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]  = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]      = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
    #        if "/" in regionText:            regionList = regionText.split('/')
            elif regionText.count(';') >= 2: regionList = regionText.split(';')
            elif "+" in regionText:          regionList = regionText.split('+')
            elif "+++" in regionText:        regionList = regionText.split('+++')
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
                record["region"] = regionName
                record["id"]     = orgID + "_" + str(regionCount)
                regionCount      = regionCount +1
                scraperwiki.sqlite.save(["id"], record)
        except: pass
    offset = offset + windowLength
    scraperwiki.sqlite.save_var("offset", offset)
scraperwiki.sqlite.save_var("offset", 0)import scraperwiki
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
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
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
    for job in root.cssselect(".jobList_table tr td"):
        record  = {}       
        jobName = job.cssselect("a.joblisteJobtitel")
        try:    jobName[0]
        except: jobName = []

        idString                      = jobName[0].attrib['href']
        index1                        = idString.rfind("=") + 1
        try:    idNumber              = idString[index1:]
        except: idNumber              = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        try:    record["id"]              = idNumber
        except: pass
        try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
        except: pass
        try:    record["tags"]            = []
        except: pass
        try:    record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect(".joblisteFirma")[0].text.strip().split()))
        except: pass
        regionText = ""
        try:    
            record["region"]          = fix_encoding_mistakes(" ".join(job.cssselect(".joblisteEinsatzorte")[0].text.strip().split())) + ", Deutschland"
            record['originalRegion']  = record['region']
            regionText = record["region"]
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass
        try:
            dateString                    = " ".join(job.cssselect("#PostedDate")[0].text.strip().split())
            if   dateString.find("Stunde") >= 0 or dateString.find("Minute") >= 0:
                record["date"]                = today
            elif dateString.find("Tag") >= 0:
                record["date"]                = dateutil.parser.parse(job.cssselect(".created_at")[0].text + "2013")
            else:
                dateOffset        = int(job.cssselect("p")[0].text.replace("Online seit","").replace("Tagen","").replace("Tag","").strip())
                record["date"] = today - timedelta(days=dateOffset)                
        except: pass
        try:    record["logoURL"]         = job.cssselect(".joblisteBodyLogo img")[0].attrib['src']
        except: pass

        record["country"]         = "de"
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(pageHTML)
            try:
                linkList = pageRoot.cssselect("#job_detail a")
                for link in linkList:
                    if link.attrib['href'].find("mailto") == -1 : record["companyURL"] = "http://" + urlparse(link.attrib['href']).hostname
            except: pass
            record["description"] = " ".join(pageRoot.cssselect("#job_detail")[0].text_content().strip().split())
        except: print sys.exc_info() # pass

        record["tags"].append("Startup")
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)

        regionList = []
        if   regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
#        if "/" in regionText:            regionList = regionText.split('/')
        elif regionText.count(';') >= 2: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
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
            record["region"] = regionName
            record["id"]     = orgID + "_" + str(regionCount)
            regionCount      = regionCount +1
            scraperwiki.sqlite.save(["id"], record)
            countNew = countNew + 1

# start: initialize variables
maxPages = 200
#baseURL  = "http://www.jobscout24.de/Jobs_Ergebnisliste.html?pg="
baseURL  = "http://www.jobscout24.de/Jobs_Ergebnisliste.html?exCrit=%3bNVJTL%3dJN008&pg="

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
    #print sUrl

    try:
        html  = scraperwiki.scrape(sUrl)
        root  = lxml.html.fromstring(html)
        scrapeTable(root)
    except: sys.exc_info()

#sys.exit()

#cleanup
count = 0
jobCount = scraperwiki.sqlite.select('count(*) FROM swdata')[0]["count(*)"]
print "Starting cleanup of ", jobCount, " rows!"
windowLength = 500
windowCount  = jobCount / windowLength
offset       = scraperwiki.sqlite.get_var("offset", 0)
for window in range(windowCount):
    rows = scraperwiki.sqlite.select('* from swdata LIMIT '+str(windowLength)+' OFFSET '+str(offset) )
    for record in rows:
        count = count + 1
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+ offset
        try:  
            record["company"] = fix_encoding_mistakes(record["company"])
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]      = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]  = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]      = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
    #        if "/" in regionText:            regionList = regionText.split('/')
            elif regionText.count(';') >= 2: regionList = regionText.split(';')
            elif "+" in regionText:          regionList = regionText.split('+')
            elif "+++" in regionText:        regionList = regionText.split('+++')
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
                record["region"] = regionName
                record["id"]     = orgID + "_" + str(regionCount)
                regionCount      = regionCount +1
                scraperwiki.sqlite.save(["id"], record)
        except: pass
    offset = offset + windowLength
    scraperwiki.sqlite.save_var("offset", offset)
scraperwiki.sqlite.save_var("offset", 0)