import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html, Cleaner
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

def scrapeTable(root, locale):
    global countNew
    try:
        for job in root.cssselect(".jobList_table .jl_odd_row, .jobList_table .jl_even_row"):
            record  = {}
            try:    jobName = job.cssselect(".jt")
            except: pass

            try:    jobName[0]
            except: continue

            idString                          = jobName[0].attrib['href']
    
            dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'", verbose=0)
            if dataAlreadySaved: 
#                print dataAlreadySaved
                continue

            try:    record["id"]              = idString
            except: print "1 ", sys.exc_info()
            try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
            except: print "2 ", sys.exc_info()
            record["company"] = ""
            try: 
                onClick = job.cssselect(".recordaffordances .recordaffordancecontainer")[1].cssselect("a")[0].attrib['onclick'].encode('utf-8')
                index1          = str(onClick).index("company:") + 8
                company = onClick[index1:].replace("'","").replace(");","").replace("web://contact","").replace("}","").strip()
                record["company"]             = company
            except: 
                try: record["company"]        = " ".join(job.cssselect(".LnkcompanyName")[0].text.strip().split())
                except: print "3 ", sys.exc_info()
            try:    
                record["region"]              = job.cssselect(".joblist_Location")[0].text.replace("Ort :","").strip()
                record['originalRegion']      = record['region']
                for phrase in redundantText:
                    record["region"]          = record["region"].replace(phrase, " ")
                record["region"]              = " ".join(record["region"].split())
            except: print "4 ", sys.exc_info()
            try:    record["logoURL"]         = job.cssselect("td a")[0].cssselect("img")[0].attrib['src']
            except: pass #print "5 ", sys.exc_info()
    
            try:
                dateString                    = " ".join(job.cssselect("#PostedDate")[0].text.strip().split()).lower()
                if   "stunde" in dateString or "hour" in dateString or "minute" in dateString or "heures" in dateString or " ore " in dateString or "siden" in dateString or " uur " in dateString or "horas" in dateString or u"λεπτά" in dateString or u"ώρες" in dateString or "timmar" in dateString:
                    record["date"]            = today
                elif "tag" in dateString or "day" in dateString or " dni " in dateString or "giorni" in dateString:
                    index1                    = dateString.find(" ")
                    index2                    = dateString.find(" ", index1+1)
                    dayNumber                 = int(dateString[index1:index2])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif "dagen" in dateString:
                    index2                    = dateString.find(" ")
                    dayNumber                 = int(dateString[:index2])           # No leading word
                    record["date"]            = today - timedelta(days=dayNumber)
                elif u"dagar" in dateString or "dagar" in dateString:              
                    #  publicerat för 3 dagar sedan 
                    offset                    = dateString.rfind(" ")
                    index1                    = dateString.rfind(" ", 0, offset)
                    index2                    = dateString.rfind(" ", 0, index1-1)
                    dayNumber                 = int(dateString[index2:index1])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif u"ημέρες" in dateString or u"día" in dateString or "jours" in dateString:              
                    #  δημοσιεύτηκε πριν από 1 ημέρες, publicado hace 2 día(s),  il y a 16 jours 
                    index1                    = dateString.rfind(" ")
                    index2                    = dateString.rfind(" ", 0, index1-1)
                    dayNumber                 = int(dateString[index2:index1])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif "woche" in dateString or "week" in dateString:
                    index1                    = dateString.find(" ")
                    index2                    = dateString.find(" ", index1+1)
                    dayNumber                 = int(dateString[index1:index2]) * 7 # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                else:
                    print "Could not parse date: ", dateString
                    record["date"]            = today
            except: print "6 ", dateString, " ", sys.exc_info()
    
            record["country"]         = locale
            try:
                cleaner          = Cleaner(scripts=True, style=True)
                pageHTML         = scraperwiki.scrape(jobName[0].attrib['href'])
                pageRoot         = lxml.html.fromstring(cleaner.clean_html(pageHTML))
                pageRootRaw      = lxml.html.fromstring(pageHTML)

                try:        record["description"]  = " ".join(pageRoot.cssselect(".content-main .content-sections")[0].text_content().strip().split())
                except: 
                    try:    record["description"]  = " ".join(pageRoot.text_content().strip().split())
                    except: pass
                try:
                    pageHTML         = scraperwiki.scrape(pageRootRaw.cssselect("#CBBody_CompanyDetailsLink")[0].attrib['href'])
                    pageRoot         = lxml.html.fromstring(pageHTML)
                    try:    record["companyURL"]   = pageRoot.cssselect("#hlWebsite")[0].attrib['href']
                    except: print "6b ", sys.exc_info()
                    try:
                        searchText = "Contact Us"
                        candidates = pageRoot.cssselect(".pContent .cpheading span.ContentHeader")
                        for candidate in candidates:
                            if searchText in candidate.text:
                                record["contactInfo"] = candidate.getparent().getparent().cssselect(".cpdcontent").text_content()
                                break
                    except: print "6c ", sys.exc_info()
                except: pass #print "6d ", sys.exc_info()
            except: print "7 ", jobName[0].attrib['href'], " ", record["description"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0) #, verbose=0

            countNew = countNew + 1
            if countNew%1000 == 0: print countNew, " jobs processed."
    except: pass # print "8 ", jobName[0].attrib['href']


# start: initialize variables
maxPages = 100 #2000
countNew = 0

#Locales not available: "fi", "hr", "bg", "li", "et", "hu", "lv", "mt", "lt", "mo", "sk", "sl", "us" , "hk", "cn", "il", "au", "jp", "in", "kr", "th", "tw"
locales  = ["de", "fr", "co.uk", "it", "dk", "be", "pl", "ch", "at", "nl", "lu", "cz", "ie", "no", "se", "es", "pt", "gr", "tw"]
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
startFound  = False
print "Start or continue from locale: ", firstLocale

#firstLocale = "co.uk"
baseURL = "http://www.careerbuilder.{0}/INTL/JobSeeker/Jobs/JobResults.aspx?excrit=QID%3dA3856738125218%3bst%3da%3buse%3dALL%3bCID%3d{1}%3bSID%3d%3f%3bTID%3d0%3bLOCCID%3d{1}%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dgt120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dIL%3bQS%3dsid_unknown%3bSS%3dNO%3bTITL%3d0%3bOB%3d-modifiedint%3bRAD%3d30%3bJQT%3dRAD%3bJDV%3dFalse%3bHost%3d{1}%3b%3bMaxLowExp%3d-1%3bRecsPerPage%3d20%3bNVJTL%3d%22JN008%22&IPath=JRCM&pg={2}"
#print baseURL.format(firstLocale, firstLocale[-2:].upper(), 6)

#sys.exit()



#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True
        try:
            baseHTML = scraperwiki.scrape(baseURL.format(locale, locale[-2:].upper(), 1))
            baseRoot = lxml.html.fromstring(baseHTML)
            maxPages=0
            try: 
                pagination = baseRoot.cssselect("#J_mxdlPaginationBottom")[0].text.strip()
                index1     = pagination.rfind(" ")+1
                maxPages   = int(pagination[index1:])
            except: print "8 ", sys.exc_info()
            if maxPages > 500: maxPages = 500 # cut new Jobs per day
            print "Scraping locale ", locale, " with ", maxPages, " pages"

            for page in range(maxPages):
                page  = page + 1
                sUrl  = baseURL.format(locale, locale[-2:].upper(), str(page))
#                print sUrl

                try:
                    html  = scraperwiki.scrape(sUrl)
                    root  = lxml.html.fromstring(html)
                    scrapeTable(root, locale)
                except: print "9 ", sys.exc_info()
            scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        except: 
            print "10 ", sys.exc_info()
print "Added ", countNew, " new jobs!"
scraperwiki.sqlite.save_var("lastLocale", locales[0]) # reset stored locale after all scraping is done

#sys.exit()
import scraperwiki
import sys
import lxml.etree
import lxml.html
from lxml.html.clean import clean_html, Cleaner
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

def scrapeTable(root, locale):
    global countNew
    try:
        for job in root.cssselect(".jobList_table .jl_odd_row, .jobList_table .jl_even_row"):
            record  = {}
            try:    jobName = job.cssselect(".jt")
            except: pass

            try:    jobName[0]
            except: continue

            idString                          = jobName[0].attrib['href']
    
            dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'", verbose=0)
            if dataAlreadySaved: 
#                print dataAlreadySaved
                continue

            try:    record["id"]              = idString
            except: print "1 ", sys.exc_info()
            try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text.strip().split()))
            except: print "2 ", sys.exc_info()
            record["company"] = ""
            try: 
                onClick = job.cssselect(".recordaffordances .recordaffordancecontainer")[1].cssselect("a")[0].attrib['onclick'].encode('utf-8')
                index1          = str(onClick).index("company:") + 8
                company = onClick[index1:].replace("'","").replace(");","").replace("web://contact","").replace("}","").strip()
                record["company"]             = company
            except: 
                try: record["company"]        = " ".join(job.cssselect(".LnkcompanyName")[0].text.strip().split())
                except: print "3 ", sys.exc_info()
            try:    
                record["region"]              = job.cssselect(".joblist_Location")[0].text.replace("Ort :","").strip()
                record['originalRegion']      = record['region']
                for phrase in redundantText:
                    record["region"]          = record["region"].replace(phrase, " ")
                record["region"]              = " ".join(record["region"].split())
            except: print "4 ", sys.exc_info()
            try:    record["logoURL"]         = job.cssselect("td a")[0].cssselect("img")[0].attrib['src']
            except: pass #print "5 ", sys.exc_info()
    
            try:
                dateString                    = " ".join(job.cssselect("#PostedDate")[0].text.strip().split()).lower()
                if   "stunde" in dateString or "hour" in dateString or "minute" in dateString or "heures" in dateString or " ore " in dateString or "siden" in dateString or " uur " in dateString or "horas" in dateString or u"λεπτά" in dateString or u"ώρες" in dateString or "timmar" in dateString:
                    record["date"]            = today
                elif "tag" in dateString or "day" in dateString or " dni " in dateString or "giorni" in dateString:
                    index1                    = dateString.find(" ")
                    index2                    = dateString.find(" ", index1+1)
                    dayNumber                 = int(dateString[index1:index2])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif "dagen" in dateString:
                    index2                    = dateString.find(" ")
                    dayNumber                 = int(dateString[:index2])           # No leading word
                    record["date"]            = today - timedelta(days=dayNumber)
                elif u"dagar" in dateString or "dagar" in dateString:              
                    #  publicerat för 3 dagar sedan 
                    offset                    = dateString.rfind(" ")
                    index1                    = dateString.rfind(" ", 0, offset)
                    index2                    = dateString.rfind(" ", 0, index1-1)
                    dayNumber                 = int(dateString[index2:index1])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif u"ημέρες" in dateString or u"día" in dateString or "jours" in dateString:              
                    #  δημοσιεύτηκε πριν από 1 ημέρες, publicado hace 2 día(s),  il y a 16 jours 
                    index1                    = dateString.rfind(" ")
                    index2                    = dateString.rfind(" ", 0, index1-1)
                    dayNumber                 = int(dateString[index2:index1])     # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                elif "woche" in dateString or "week" in dateString:
                    index1                    = dateString.find(" ")
                    index2                    = dateString.find(" ", index1+1)
                    dayNumber                 = int(dateString[index1:index2]) * 7 # Remove leading word "Vor ", "posted", ...
                    record["date"]            = today - timedelta(days=dayNumber)
                else:
                    print "Could not parse date: ", dateString
                    record["date"]            = today
            except: print "6 ", dateString, " ", sys.exc_info()
    
            record["country"]         = locale
            try:
                cleaner          = Cleaner(scripts=True, style=True)
                pageHTML         = scraperwiki.scrape(jobName[0].attrib['href'])
                pageRoot         = lxml.html.fromstring(cleaner.clean_html(pageHTML))
                pageRootRaw      = lxml.html.fromstring(pageHTML)

                try:        record["description"]  = " ".join(pageRoot.cssselect(".content-main .content-sections")[0].text_content().strip().split())
                except: 
                    try:    record["description"]  = " ".join(pageRoot.text_content().strip().split())
                    except: pass
                try:
                    pageHTML         = scraperwiki.scrape(pageRootRaw.cssselect("#CBBody_CompanyDetailsLink")[0].attrib['href'])
                    pageRoot         = lxml.html.fromstring(pageHTML)
                    try:    record["companyURL"]   = pageRoot.cssselect("#hlWebsite")[0].attrib['href']
                    except: print "6b ", sys.exc_info()
                    try:
                        searchText = "Contact Us"
                        candidates = pageRoot.cssselect(".pContent .cpheading span.ContentHeader")
                        for candidate in candidates:
                            if searchText in candidate.text:
                                record["contactInfo"] = candidate.getparent().getparent().cssselect(".cpdcontent").text_content()
                                break
                    except: print "6c ", sys.exc_info()
                except: pass #print "6d ", sys.exc_info()
            except: print "7 ", jobName[0].attrib['href'], " ", record["description"]
    
            #save in datastore
            scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0) #, verbose=0

            countNew = countNew + 1
            if countNew%1000 == 0: print countNew, " jobs processed."
    except: pass # print "8 ", jobName[0].attrib['href']


# start: initialize variables
maxPages = 100 #2000
countNew = 0

#Locales not available: "fi", "hr", "bg", "li", "et", "hu", "lv", "mt", "lt", "mo", "sk", "sl", "us" , "hk", "cn", "il", "au", "jp", "in", "kr", "th", "tw"
locales  = ["de", "fr", "co.uk", "it", "dk", "be", "pl", "ch", "at", "nl", "lu", "cz", "ie", "no", "se", "es", "pt", "gr", "tw"]
firstLocale = scraperwiki.sqlite.get_var("lastLocale", locales[0])
startFound  = False
print "Start or continue from locale: ", firstLocale

#firstLocale = "co.uk"
baseURL = "http://www.careerbuilder.{0}/INTL/JobSeeker/Jobs/JobResults.aspx?excrit=QID%3dA3856738125218%3bst%3da%3buse%3dALL%3bCID%3d{1}%3bSID%3d%3f%3bTID%3d0%3bLOCCID%3d{1}%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bPDQ%3dAll%3bPAYL%3d0%3bPAYH%3dgt120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dIL%3bQS%3dsid_unknown%3bSS%3dNO%3bTITL%3d0%3bOB%3d-modifiedint%3bRAD%3d30%3bJQT%3dRAD%3bJDV%3dFalse%3bHost%3d{1}%3b%3bMaxLowExp%3d-1%3bRecsPerPage%3d20%3bNVJTL%3d%22JN008%22&IPath=JRCM&pg={2}"
#print baseURL.format(firstLocale, firstLocale[-2:].upper(), 6)

#sys.exit()



#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for locale in locales:
    if firstLocale == locale or startFound:
        startFound = True
        try:
            baseHTML = scraperwiki.scrape(baseURL.format(locale, locale[-2:].upper(), 1))
            baseRoot = lxml.html.fromstring(baseHTML)
            maxPages=0
            try: 
                pagination = baseRoot.cssselect("#J_mxdlPaginationBottom")[0].text.strip()
                index1     = pagination.rfind(" ")+1
                maxPages   = int(pagination[index1:])
            except: print "8 ", sys.exc_info()
            if maxPages > 500: maxPages = 500 # cut new Jobs per day
            print "Scraping locale ", locale, " with ", maxPages, " pages"

            for page in range(maxPages):
                page  = page + 1
                sUrl  = baseURL.format(locale, locale[-2:].upper(), str(page))
#                print sUrl

                try:
                    html  = scraperwiki.scrape(sUrl)
                    root  = lxml.html.fromstring(html)
                    scrapeTable(root, locale)
                except: print "9 ", sys.exc_info()
            scraperwiki.sqlite.save_var("lastLocale", locale) # store the last locale that was scraped
        except: 
            print "10 ", sys.exc_info()
print "Added ", countNew, " new jobs!"
scraperwiki.sqlite.save_var("lastLocale", locales[0]) # reset stored locale after all scraping is done

#sys.exit()
