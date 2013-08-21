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

redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))

def scrapeTable(root):
    global scrapeCount
    for job in root.cssselect("table.summary tr.STDsrRes, table.summary tr.gold"):
        record  = {}
        jobName = job.cssselect("td:first-child a")
        try:    jobName[0]
        except: continue

        idString                          = jobName[0].attrib['href']
        index1                            = idString.find("/", 7) + 1 # offset of 7 to start within "result" exemplary url is: "/job/result/10423087/107"
        try:    idNumber                  = idString[index1:idString.find("?")]
        except: idNumber                  = idString

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idNumber+"'", verbose=0) 
        if dataAlreadySaved: continue

        record["id"]                      = idNumber
        record["name"]                    = " ".join(jobName[0].text_content().strip().split())
        try:    record["company"]         = " ".join(job.cssselect("td:nth-child(2) a")[0].text.strip().split())
        except: pass
        try:
            record["country"]             = "us"
            record["region"]              = " ".join(job.cssselect("td:nth-child(3)")[0].text_content().strip().split()) + ", USA"
            record['originalRegion']      = record['region']
            for phrase in redundantText:
                record["region"]          = record["region"].replace(phrase, " ").strip()
            record["region"]     = re.sub("^- ", "", record["region"]).strip()
            record["region"]     = re.sub("^, ", "", record["region"]).strip()
        except: pass
        try:    record["date"]            = dateutil.parser.parse(job.cssselect("td:nth-child(4)")[0].text.strip())
        except: pass

        try:
            pageHTML                      = scraperwiki.scrape("http://www.dice.com"+jobName[0].attrib['href'])
            pageRoot                      = lxml.html.fromstring(pageHTML)
            try:    record["description"] = " ".join(lxml.html.fromstring(clean_html(pageHTML)).cssselect("#descriptionCol")[0].text_content().strip().split())
            except: record["description"] = " ".join(lxml.html.fromstring(clean_html(pageHTML)).cssselect("body")[0].text_content().strip().split())
            try:    record["tags"]        = pageRoot.cssselect("#jobOverview .pane:nth-child(2) dl dd")[0].text.strip().split()
            except: pass
            try:    record["logoURL"]     = pageRoot.cssselect(".companyLogo img")[0].attrib['src']
            except: record["logoURL"]     = pageRoot.cssselect("img[src*=logo]")[0].attrib['src']
            try:    record["companyURL"]  = pageRoot.cssselect("#contactInfo a[href^=http]")[0].attrib['href']
            except: pass
            try:    record["contactInfo"] = " ".join(pageRoot.cssselect("#contactInfo")[0].text_content().strip().split())
            except: pass
        except: pass

        #save in datastore
#        scraperwiki.sqlite.save(["id"], record)
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)
        scrapeCount = scrapeCount + 1

# start: initialize variables
scrapeCount = 0
baseURL  = "http://www.dice.com/job/results?x=all&o="
offset = scraperwiki.sqlite.get_var("offset", 0)
if offset == None: offset=0
startFound = False
print "Start or continue from offset: ", offset
maxPages = 500 - offset #2811 - offset

#scraperwiki.sqlite.execute("drop table if exists swdata")
#try:    scraperwiki.sqlite.execute("create table swdata (id)")
#except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page
    sUrl  = baseURL + str((offset + page) * 30)
#    print sUrl

    html  = scraperwiki.scrape(sUrl)
    root  = lxml.html.fromstring(html)
    scrapeTable(root)
    scraperwiki.sqlite.save_var("offset", page+offset+1) # store the last locale that was scraped
scraperwiki.sqlite.save_var("offset", 0) # reset stored locale after all scraping is done

# Cleanup
#totalNumberOfJobs = scraperwiki.sqlite.select("count(*) from swdata")[0]["count(*)"]
#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (description IS NULL OR region IS NULL OR company IS NULL)")
#scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (description='' OR region='' OR company='')")
#scraperwiki.sqlite.commit()
#cleanedNumberOfJobs = scraperwiki.sqlite.select("count(*) from swdata")[0]["count(*)"]
#print "Removed: ", totalNumberOfJobs - cleanedNumberOfJobs, " jobs without description, region or company."
