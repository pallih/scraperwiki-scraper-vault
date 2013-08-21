import scraperwiki
import sys
import lxml.etree
import lxml.html
#from lxml.html.clean import clean_html
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

def scrapeTable(root):
    for job in root.cssselect(".jobs-list .beitrag-job"):
        record = {}       
        jobName = job.cssselect(".beitrags-inhalt a")
        try:    jobName[0]
        except: jobName = []

        idString         = jobName[0].attrib['href']

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'")
        if dataAlreadySaved: continue

        record["id"]                      = idString
        try:    record["name"]            = " ".join(jobName[0].text.strip().split())
        except: pass
        try:    record["tags"]            = ["Startup"]
        except: pass
        try:    record["logoURL"]         = job.cssselect(".meta-jobs-img")[0].attrib['src']
        except: pass
        try:    
            dateOffset                    = int(job.cssselect("p")[0].text.replace("Vor","").replace("Tagen","").replace("Tag","").strip())
            record["date"]                = today - timedelta(days=dateOffset)
        except: pass

        try:
            pageHTML                      = scraperwiki.scrape("http://www.deutsche-startups.de" + jobName[0].attrib['href'])
            pageRoot                      = lxml.html.fromstring(pageHTML)
            try:    record["description"] = " ".join(pageRoot.cssselect("#beitrag-job-item")[0].text_content().strip().split())
            except: pass
            try:    record["company"]     = " ".join(pageRoot.cssselect(".beitrags-inhalt table tr")[0].cssselect("td")[1].cssselect("b")[0].text_content().strip().split())
            except: pass
            try:    record["country"]     = "de"
            except: pass
            try:    record["logoURL"]     = pageRoot.cssselect(".meta-jobs-img")[0].attrib['src']
            except: pass
            try:    record["companyURL"]  = pageRoot.cssselect(".beitrags-inhalt table tr")[2].cssselect("td")[1].cssselect("a")[0].attrib['href']
            except: pass
            try:    record["region"]      = " ".join(pageRoot.cssselect(".beitrags-inhalt table tr")[5].cssselect("td")[1].cssselect("b")[0].text.strip().split())
            except: pass
            try:    record["originalRegion"]      = " ".join(pageRoot.cssselect(".beitrags-inhalt table tr")[5].cssselect("td")[1].cssselect("b")[0].text.strip().split())
            except: pass
        except: print sys.exc_info() # pass

        #save in datastore
        scraperwiki.sqlite.save(["id"], data=record, table_name='swdata', verbose=0)

# start: initialize variables
maxPages = 10
baseURL  = "http://www.deutsche-startups.de/startups-jobs/stellenangebote/?paged="

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
    page  = page + 1
    sUrl  = baseURL + str(page)
#    print sUrl

    try:
        html  = scraperwiki.scrape(sUrl)
        root  = lxml.html.fromstring(html)
        scrapeTable(root)
    except: print sys.exc_info() # pass

