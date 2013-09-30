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
from datetime import datetime, date, time
import re

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() #pass

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

def scrapeTable(root, locale, countNew):
    for job in root.cssselect("div#primaryResults table tr.odd, div#primaryResults table tr.even"):
        record = {}       

        jobName = job.cssselect("div.jobTitleContainer a")
        try:    jobName[0]
        except: jobName = []

        idNumber                      = " ".join(jobName[0].attrib['name'].strip().split())

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["name"]            = " ".join(jobName[0].text.strip().split())
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(clean_html(pageHTML))
            record["description"] = " ".join(pageRoot.text_content().strip().split())
        except: print sys.exc_info() # pass

        onClick      = jobName[0].attrib['onclick']
        index1       = str(onClick).index("AVSDM") + 6
        try:    date = onClick[index1:index1 + 16]
        except: date = ""
        record["date"]            = dateutil.parser.parse(date)  #time.strptime(date, '%Y-%m-%d %H:%M')

        try:
            record["company"] = " ".join(fix_encoding_mistakes(job.cssselect(".companyContainer div.companyConfidential")[0].text.strip()).split())
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    record["country"] = locale
        except: pass
        try:    record["logoURL"] = job.cssselect("a.companyLogo img")[0].attrib['src']
        except:
            try:record["logoURL"] = pageRoot.cssselect("div#jobPostingLogo img")[0].attrib['src']
            except: pass
        record["region"] = ""
        regionText = ""
        try:
            record["region"]      = fix_encoding_mistakes(job.cssselect(".jobLocationSingleLine a")[0].attrib['title'])
            record['originalRegion']  = record['region']
            regionText = record["region"]
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)
        countNew = countNew + 1

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
    return countNew

# start: initialize variables
countNew = 0
maxPages = 50
#baseURL  = "http://jobsuche.monster.de/Jobs/?q=IT&pg="
baseURL  = "http://jobsearch.monster.com/jobs/IT-Software-Development_4?pg="
locales  = ["de", "fr", "uk", "it", "dk", "be", "pl", "ch", "at", "nl", "lu", "cz", "ie", "no", "se", "fi", "es", "pt", "hr", "bg", "li", "et", "gr", "hu", "lv", "lt", "mt", "mo", "sk", "sl", "us", "hk", "cn", "il", "au", "jp", "in", "kr", "th", "tw"]
# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
if firstLocale == None: firstLocale="de"
startFound  = False
print "Start or continue from locale: ", firstLocale

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True 
        for page in range(maxPages):
            page  = page + 1
            sUrl  = baseURL + str(page) + "&cy=" + str(locale)
        
            html  = scraperwiki.scrape(sUrl)
            root  = lxml.html.fromstring(html)
            try:
                currentPage = int(root.cssselect(".navLinks .boxWrap.selected a")[0].text.strip())
                if page != currentPage: break
            except:
                print "Problems with locale: ", locale, " - no data? ", sUrl 
                break
            countNew = scrapeTable(root, locale, countNew)
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        print "Completed locale: ", locale
    else:
        print "Skipped locale: ", locale
print "Added ", countNew, " new jobs!"
scraperwiki.sqlite.save_var("lastLocale", locales[0]) # reset stored locale after all scraping is done

sys.exit()

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
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+offset
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
from datetime import datetime, date, time
import re

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() #pass

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

def scrapeTable(root, locale, countNew):
    for job in root.cssselect("div#primaryResults table tr.odd, div#primaryResults table tr.even"):
        record = {}       

        jobName = job.cssselect("div.jobTitleContainer a")
        try:    jobName[0]
        except: jobName = []

        idNumber                      = " ".join(jobName[0].attrib['name'].strip().split())

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'")
        if dataAlreadySaved: continue

        record["id"]              = idNumber
        record["name"]            = " ".join(jobName[0].text.strip().split())
        try:
            pageHTML              = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot              = lxml.html.fromstring(clean_html(pageHTML))
            record["description"] = " ".join(pageRoot.text_content().strip().split())
        except: print sys.exc_info() # pass

        onClick      = jobName[0].attrib['onclick']
        index1       = str(onClick).index("AVSDM") + 6
        try:    date = onClick[index1:index1 + 16]
        except: date = ""
        record["date"]            = dateutil.parser.parse(date)  #time.strptime(date, '%Y-%m-%d %H:%M')

        try:
            record["company"] = " ".join(fix_encoding_mistakes(job.cssselect(".companyContainer div.companyConfidential")[0].text.strip()).split())
            record["company"] = re.sub("^- ", "", record["company"]).strip()
            for phrase in redundantText:
                record["company"]  = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    record["country"] = locale
        except: pass
        try:    record["logoURL"] = job.cssselect("a.companyLogo img")[0].attrib['src']
        except:
            try:record["logoURL"] = pageRoot.cssselect("div#jobPostingLogo img")[0].attrib['src']
            except: pass
        record["region"] = ""
        regionText = ""
        try:
            record["region"]      = fix_encoding_mistakes(job.cssselect(".jobLocationSingleLine a")[0].attrib['title'])
            record['originalRegion']  = record['region']
            regionText = record["region"]
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass
        #save in datastore
        scraperwiki.sqlite.save(["id"], record)
        countNew = countNew + 1

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
    return countNew

# start: initialize variables
countNew = 0
maxPages = 50
#baseURL  = "http://jobsuche.monster.de/Jobs/?q=IT&pg="
baseURL  = "http://jobsearch.monster.com/jobs/IT-Software-Development_4?pg="
locales  = ["de", "fr", "uk", "it", "dk", "be", "pl", "ch", "at", "nl", "lu", "cz", "ie", "no", "se", "fi", "es", "pt", "hr", "bg", "li", "et", "gr", "hu", "lv", "lt", "mt", "mo", "sk", "sl", "us", "hk", "cn", "il", "au", "jp", "in", "kr", "th", "tw"]
# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
if firstLocale == None: firstLocale="de"
startFound  = False
print "Start or continue from locale: ", firstLocale

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True 
        for page in range(maxPages):
            page  = page + 1
            sUrl  = baseURL + str(page) + "&cy=" + str(locale)
        
            html  = scraperwiki.scrape(sUrl)
            root  = lxml.html.fromstring(html)
            try:
                currentPage = int(root.cssselect(".navLinks .boxWrap.selected a")[0].text.strip())
                if page != currentPage: break
            except:
                print "Problems with locale: ", locale, " - no data? ", sUrl 
                break
            countNew = scrapeTable(root, locale, countNew)
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        print "Completed locale: ", locale
    else:
        print "Skipped locale: ", locale
print "Added ", countNew, " new jobs!"
scraperwiki.sqlite.save_var("lastLocale", locales[0]) # reset stored locale after all scraping is done

sys.exit()

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
        if count%1000 == 0: print count, " jobs processed - up to ID: ", 1000+offset
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

