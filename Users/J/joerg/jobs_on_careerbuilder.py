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
    for job in root.cssselect(".jl_tbl tr.prefRow"):
        record  = {}
        try:    jobName = job.cssselect(".prefTitle")
        except: pass

        try:    jobName[0]
        except: continue

        idString                          = jobName[0].attrib['href']

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'", verbose=0)
        if dataAlreadySaved:
#           print dataAlreadySaved
            continue

        try:    record["id"]              = idString
        except: pass
        try:    record["name"]            = fix_encoding_mistakes(" ".join(jobName[0].text().split()))
        except: pass
        try:    record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect("a.prefCompany")[0].text_content().split()))
        except:
            try:record["company"]         = fix_encoding_mistakes(" ".join(job.cssselect("span.prefCompany")[0].text_content().split()))
            except: pass#print "No company for ", job.text_content()
        try:    
            regionText          = job.cssselect("td")[5].text_content().split("-")
            record['originalRegion']  = regionText
            record["region"]    = regionText[1].strip() + ", " + regionText[0].strip() + ", USA"
        except: print "1 ", sys.exc_info()
        try:
            dateString                    = " ".join(job.cssselect(".jl_rslt_posted_cell span")[0].text.strip().split())
            if   dateString.find("Today") >= 0:
                record["date"]            = today
            elif dateString.find("Yesterday") >= 0:
                record["date"]            = today - timedelta(days=1)
            elif dateString.find("Days Ago") >= 0:
                index1                    = dateString.find(" ")
                dayNumber                 = int(dateString[0:index1])
                record["date"]            = today - timedelta(days=dayNumber)
            elif dateString.find("Week Ago") >= 0:
                index1                    = dateString.find(" ")
                dayNumber                 = int(dateString[0:index1]) * 7
                record["date"]            = today - timedelta(days=dayNumber)
            elif dateString.find("Weeks Ago") >= 0:
                index1                    = dateString.find(" ")
                dayNumber                 = int(dateString[0:index1]) * 7
                record["date"]            = today - timedelta(days=dayNumber)
#            elif dateString.find("Tag") >= 0:
#                record["date"]                = dateutil.parser.parse(job.cssselect(".created_at")[0].text + "2013")
# parse job.cssselect(".jl_rslt_posted_cell span")[0].attrib['title']
            else:
                print "Could not parse date: ", dateString

        except: print "2 ", dateString, sys.exc_info()

#        record["country"]         = "de"
        try:
            cleaner          = Cleaner(scripts=True, style=True)
            pageHTML         = scraperwiki.scrape(jobName[0].attrib['href'])
            pageRoot         = lxml.html.fromstring(cleaner.clean_html(pageHTML))
            pageRootRaw      = lxml.html.fromstring(pageHTML)

            try:    record["description"]  = " ".join(pageRoot.cssselect(".content-main .content-sections")[0].text_content().split())
            except: 
                try:record["description"]  = " ".join(pageRoot.text_content().split())
                except: print "3 ", sys.exc_info()
            try:     record["logoURL"]     = pageRootRaw.cssselect("#imgLogo")[0].attrib['src']
            except: 
                try: record["logoURL"]     = pageRootRaw.cssselect("#CBBody_CompanyImage")[0].attrib['src']
                except: pass # print "3 ", sys.exc_info()

            try:
                pageHTML         = scraperwiki.scrape(pageRootRaw.cssselect("#CBBody_CompanyDetailsLink")[0].attrib['href'])
                pageRoot         = lxml.html.fromstring(pageHTML)
                try:    record["companyURL"]   = pageRoot.cssselect("#hlWebsite")[0].attrib['href']
                except: print "4 ", sys.exc_info()
                try:    
                    searchText = "Contact Us"
                    candidates = pageRoot.cssselect(".pContent .cpheading span.ContentHeader")
                    for candidate in candidates:
                        if searchText in candidate.text:
                            record["contactInfo"] = candidate.getparent().getparent().cssselect(".cpdcontent").text_content()
                            break
                except: print "5 ", sys.exc_info()
            except: pass #print "5b ", sys.exc_info()

        except: pass #print "6 ", pageHTML

        #save in datastore
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 2000 #2000
#baseURL  = "http://www.jobscout24.de/Jobs_Ergebnisliste.html?pg="
baseURL  = "http://www.careerbuilder.com/JobSeeker/Jobs/JobResults.aspx?excrit=QID%3dA3856730825968%3bst%3dA%3buse%3dALL%3bCID%3dUS%3bSID%3d%3f%3bTID%3d0%3bENR%3dNO%3bDTP%3dDRNS%3bYDI%3dYES%3bIND%3dALL%3bPDQ%3dAll%3bJN%3dJN008%3bPAYL%3d0%3bPAYH%3dGT120%3bPOY%3dNO%3bETD%3dALL%3bRE%3dALL%3bMGT%3dDC%3bSUP%3dDC%3bFRE%3d30%3bCHL%3dAL%3bQS%3dSID_UNKNOWN%3bSS%3dNO%3bTITL%3d0%3bOB%3d-modifiedint%3bRAD%3d30%3bJQT%3dRAD%3bJDV%3dFalse%3bHost%3dUS%3bMaxLowExp%3d-1%3bRecsPerPage%3d25&pg="

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
    except: print "7 ", sUrl

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