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

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass

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
    for job in root.cssselect("div.joblisting"):
        record = {}

        idNumber                  = job.cssselect("div.joblisting")[0].attrib['id'][11:]

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'", verbose=0)
        if dataAlreadySaved: continue

        try:    record["id"]      = idNumber
        except: pass
        try:    record["name"]    = " ".join(job.cssselect("div.job_title a span")[0].text.strip().split()) 
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect("div.job_date_added time")[0].attrib['datetime'])
        except: pass
        record["region"]          = ""
        try:    
            record["region"]      = job.cssselect(".job_location .locality span")[0].text.strip()
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass

        record["country"]         = locale       #TODO: parse region(s)?
        try:
            record["company"]     = " ".join(fix_encoding_mistakes(job.cssselect("div.company_name span")[0].text.strip()).split())
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
            record["company"]     = re.sub("^- ", "", record["company"]).strip()
        except: pass
        try: record["logoURL"]    = job.cssselect("div.company_logo img")[0].attrib['src']
        except: pass

        try:
            pageHTML              = scraperwiki.scrape("http://www.stepstone.de"+job.cssselect("div.job_title a")[0].get("href"))
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["description"] = " ".join(pageRoot.cssselect("iframe")[0].text_content().strip().split())
            record["companyURL"] = "http://" + urlparse(pageRoot.cssselect("iframe a")[0].attrib['href']).hostname
        except: pass

        try:
            pageHTML              = scraperwiki.scrape("http://www.stepstone.de"+job.cssselect("div.company_logo a")[0].get("href"))
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["contactInfo"] = " ".join(pageRoot.cssselect(".contact_info")[0].text_content().strip().split())

            address = dict()
            try: address["street"]       = " ".join(pageRoot.cssselect(".contact_info .street-address")[0].text_content().strip().split())
            except: pass
            try: address["postalCode"]   = " ".join(pageRoot.cssselect(".contact_info .postal-code")[0].text_content().strip().split())
            except: pass
            try: address["city"]         = " ".join(pageRoot.cssselect(".contact_info .locality")[0].text_content().strip().split())
            except: pass
            try: address["country"]      = " ".join(pageRoot.cssselect(".contact_info .country-name")[0].text_content().strip().split())
            except: pass
            try: address["companyURL"]   = pageRoot.cssselect(".company_website a")[0].attrib['href']
            except: pass
            try: address["companyEmail"] = " ".join(pageRoot.cssselect(".company_email a")[0].text_content().strip().split())
            except: pass
            record["contactInfoStructured"] = address

            record["companyURL"] = pageRoot.cssselect(".company_website a")[0].attrib['href']
        except: pass

#        scraperwiki.sqlite.save(["id"], record)
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)
        countNew = countNew + 1

        regionList = []
        regionText = record["region"]
        if   regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 2: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
#        elif "/" in regionText:          regionList = regionText.split('/')
#        elif "-" in regionText:          regionList = regionText.split('-')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " und/oder " in regionText: regionList = regionText.split(' und/oder ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        elif " and/or " in regionText:   regionList = regionText.split(' and/or ')
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
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)
            countNew = countNew + 1
    return countNew

#start
countNew = 0
baseURL1 = "http://www.stepstone."
baseURL2 = "/5/job-search-simple.html?offset="
locales  = ["de", "fr", "dk", "be", "se", "nl", "at", "it", "lu", "no"]
# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
startFound  = False
print "Start or continue from locale: ", firstLocale

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' already exists."

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True 
        baseHTML = scraperwiki.scrape(baseURL1 + locale + baseURL2 + "1")
        baseRoot = lxml.html.fromstring(baseHTML)
        maxPages=0
        try: maxPages = int(baseRoot.cssselect(".navigation_outof")[0].attrib['title'])
        except: pass
        if maxPages > 300: maxPages = 300 # cut new Jobs per day
        print "Scraping locale ", locale, " with ", maxPages, " pages"
        for page in range(maxPages):
            page  = page 
            sUrl  = baseURL1 + locale + baseURL2 + str(page * 25)
        
            try:
                html  = scraperwiki.scrape(sUrl)
                root  = lxml.html.fromstring(html)
                countNew = scrapeTable(root, locale, countNew)
            except: 
                print sys.exc_info()
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
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
            record["company"]     = fix_encoding_mistakes(record["company"])
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]       = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]   = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]     = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"] = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
            elif regionText.count('/') >= 3: regionList = regionText.split('/')
    #        elif "/" in regionText:          regionList = regionText.split('/')
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
import time
import dateutil.parser
from datetime import datetime, date, time
import re

# List of text phrases to be removed from data (how to handle "(Raum "...")" ?)
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    try:    redundantText.append(row[0].decode('utf-8'))
    except: print sys.exc_info() # pass

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
    for job in root.cssselect("div.joblisting"):
        record = {}

        idNumber                  = job.cssselect("div.joblisting")[0].attrib['id'][11:]

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'", verbose=0)
        if dataAlreadySaved: continue

        try:    record["id"]      = idNumber
        except: pass
        try:    record["name"]    = " ".join(job.cssselect("div.job_title a span")[0].text.strip().split()) 
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect("div.job_date_added time")[0].attrib['datetime'])
        except: pass
        record["region"]          = ""
        try:    
            record["region"]      = job.cssselect(".job_location .locality span")[0].text.strip()
            record['originalRegion']  = record['region']
            for phrase in redundantText:
                record["region"]  = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass

        record["country"]         = locale       #TODO: parse region(s)?
        try:
            record["company"]     = " ".join(fix_encoding_mistakes(job.cssselect("div.company_name span")[0].text.strip()).split())
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
            record["company"]     = re.sub("^- ", "", record["company"]).strip()
        except: pass
        try: record["logoURL"]    = job.cssselect("div.company_logo img")[0].attrib['src']
        except: pass

        try:
            pageHTML              = scraperwiki.scrape("http://www.stepstone.de"+job.cssselect("div.job_title a")[0].get("href"))
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["description"] = " ".join(pageRoot.cssselect("iframe")[0].text_content().strip().split())
            record["companyURL"] = "http://" + urlparse(pageRoot.cssselect("iframe a")[0].attrib['href']).hostname
        except: pass

        try:
            pageHTML              = scraperwiki.scrape("http://www.stepstone.de"+job.cssselect("div.company_logo a")[0].get("href"))
            pageRoot              = lxml.html.fromstring(pageHTML)
            record["contactInfo"] = " ".join(pageRoot.cssselect(".contact_info")[0].text_content().strip().split())

            address = dict()
            try: address["street"]       = " ".join(pageRoot.cssselect(".contact_info .street-address")[0].text_content().strip().split())
            except: pass
            try: address["postalCode"]   = " ".join(pageRoot.cssselect(".contact_info .postal-code")[0].text_content().strip().split())
            except: pass
            try: address["city"]         = " ".join(pageRoot.cssselect(".contact_info .locality")[0].text_content().strip().split())
            except: pass
            try: address["country"]      = " ".join(pageRoot.cssselect(".contact_info .country-name")[0].text_content().strip().split())
            except: pass
            try: address["companyURL"]   = pageRoot.cssselect(".company_website a")[0].attrib['href']
            except: pass
            try: address["companyEmail"] = " ".join(pageRoot.cssselect(".company_email a")[0].text_content().strip().split())
            except: pass
            record["contactInfoStructured"] = address

            record["companyURL"] = pageRoot.cssselect(".company_website a")[0].attrib['href']
        except: pass

#        scraperwiki.sqlite.save(["id"], record)
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)
        countNew = countNew + 1

        regionList = []
        regionText = record["region"]
        if   regionText.count(',') >= 2: regionList = regionText.split(',')
        elif regionText.count('/') >= 3: regionList = regionText.split('/')
        elif regionText.count(';') >= 2: regionList = regionText.split(';')
        elif "+" in regionText:          regionList = regionText.split('+')
        elif "+++" in regionText:        regionList = regionText.split('+++')
#        elif "/" in regionText:          regionList = regionText.split('/')
#        elif "-" in regionText:          regionList = regionText.split('-')
        elif " oder " in regionText:     regionList = regionText.split(' oder ')
        elif " und " in regionText:      regionList = regionText.split(' und ')
        elif " und/oder " in regionText: regionList = regionText.split(' und/oder ')
        elif " and " in regionText:      regionList = regionText.split(' and ')
        elif " or " in regionText:       regionList = regionText.split(' or ')
        elif " and/or " in regionText:   regionList = regionText.split(' and/or ')
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
#            scraperwiki.sqlite.save(["id"], record)
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)
            countNew = countNew + 1
    return countNew

#start
countNew = 0
baseURL1 = "http://www.stepstone."
baseURL2 = "/5/job-search-simple.html?offset="
locales  = ["de", "fr", "dk", "be", "se", "nl", "at", "it", "lu", "no"]
# recover after interruptions (e.g., CPUTimeExceededError)
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
startFound  = False
print "Start or continue from locale: ", firstLocale

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' already exists."

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True 
        baseHTML = scraperwiki.scrape(baseURL1 + locale + baseURL2 + "1")
        baseRoot = lxml.html.fromstring(baseHTML)
        maxPages=0
        try: maxPages = int(baseRoot.cssselect(".navigation_outof")[0].attrib['title'])
        except: pass
        if maxPages > 300: maxPages = 300 # cut new Jobs per day
        print "Scraping locale ", locale, " with ", maxPages, " pages"
        for page in range(maxPages):
            page  = page 
            sUrl  = baseURL1 + locale + baseURL2 + str(page * 25)
        
            try:
                html  = scraperwiki.scrape(sUrl)
                root  = lxml.html.fromstring(html)
                countNew = scrapeTable(root, locale, countNew)
            except: 
                print sys.exc_info()
        scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
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
            record["company"]     = fix_encoding_mistakes(record["company"])
            for phrase in redundantText:
                record["company"] = record["company"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["name"]       = fix_encoding_mistakes(record["name"])
            for phrase in redundantText:
                record["name"]   = record["name"].replace(phrase, " ").strip()
        except: pass
        try:    
            record["region"]     = fix_encoding_mistakes(record["region"])
            for phrase in redundantText:
                record["region"] = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
            scraperwiki.sqlite.save(["id"], record)
    
            regionList = []
            regionText = record["region"]
            if   regionText.count(',') >= 2: regionList = regionText.split(',')
            elif regionText.count('/') >= 3: regionList = regionText.split('/')
    #        elif "/" in regionText:          regionList = regionText.split('/')
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
