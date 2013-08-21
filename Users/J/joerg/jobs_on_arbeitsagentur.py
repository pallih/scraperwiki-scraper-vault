import scraperwiki
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

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

# List of text phrases to be removed from data
redundantText = []
redundantPhrasesFile = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0Aoevfvsr8NYhdHRlS1RtS2ViYVFPeFJFRG5lSGtyRlE&single=true&gid=0&output=csv")
reader = csv.reader(redundantPhrasesFile.splitlines())
for row in reader:
    redundantText.append(row[0].decode('utf-8'))

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
    global countNew
    for job in root.cssselect("#tabellenanfang tbody tr"):
        record = {}

        jobName = job.cssselect("a.primaerElement")
        try:    jobName[0]
        except: continue
        idString                          = jobName[0].attrib['href']

        dataAlreadySaved = scraperwiki.sqlite.select("* from swdata where id='"+idString+"'")
        if dataAlreadySaved: continue

        try:    record["id"]      = idString
        except: pass
        try:    record["name"]    = " ".join(jobName[0].text_content().strip().split())
        except: pass
        try:    record["date"]    = dateutil.parser.parse(job.cssselect("td")[1].text_content().strip())
        except: pass
        try:    record["region"]  = fix_encoding_mistakes(" ".join(job.cssselect("td")[3].text_content().strip().split())) + ", Deutschland"
        except: record["region"]  = ""
        try:    record["originalRegion"]  = fix_encoding_mistakes(" ".join(job.cssselect("td")[3].text_content().strip().split())) + ", Deutschland"
        except: record["originalRegion"]  = ""
        try:    record["company"] = " ".join(job.cssselect("td")[2].text_content().strip().split())
        except: pass

        try:
            pageHTML                       = scraperwiki.scrape("http://jobboerse.arbeitsagentur.de/" + jobName[0].attrib['href'])
            pageRoot                       = lxml.html.fromstring(pageHTML)
            try: record["description"]     = " ".join(pageRoot.cssselect(".containerStrukturierteDatenansicht")[0].text_content().strip().split())
            except: record["description"]  = " ".join(pageRoot.cssselect("body")[0].text_content().strip().split())
#            try: record["contactInfo"]     = " ".join(pageRoot.cssselect("#eingabemaske .ersteBox .cf")[1].cssselect("p")[0].text_content().strip().split())
#            except: pass

            try:
                searchText = "fragen und Bewerbungen an" # should be "Rückfragen und Bewerbungen an" (ignore umlaute!)
                candidates = pageRoot.cssselect("#eingabemaske .labelText")
                for candidate in candidates:
                    if searchText in candidate.text:
                        record["contactInfo"] = candidate.getparent().text_content()
                        break
                record["contactInfo"]  = record["contactInfo"].replace(u"Rückfragen und Bewerbungen an", "").strip()
                record["contactInfo"]  = record["contactInfo"].replace("Rückfragen und Bewerbungen an", "").strip()
#                print record["contactInfo"]
            except: pass

            try: record["companyURL"]      = pageRoot.cssselect("#eingabemaske .ersteBox .cf:last-child a")[0].text_content()
            except: pass
            try: record["logoURL"]         = "http://jobboerse.arbeitsagentur.de/" + pageRoot.cssselect("#logoarbeitgeber")[0].attrib['src']
            except: record["logoURL"]      = "http://jobboerse.arbeitsagentur.de/" + pageRoot.cssselect("#aglogo")[0].attrib['src']
        except: pass

        scraperwiki.sqlite.save(["id"], record)        
        countNew = countNew + 1
        if countNew%100 == 0: print countNew, "Jobs processed."

#start
countNew = 0
maxPages = 200 # max is 200 (10 per page)

sUrl  = "http://jobboerse.arbeitsagentur.de/vamJB/klicksuche.html?kgr=as&m=4&aa=1&e1=75855"

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (id)")
except: print "Table 'swdata' probably already exists."

for page in range(maxPages):
#    print sUrl
    # The site we will navigate into, handling it's session
    r = br.open(sUrl)
    html = r.read()

    root  = lxml.html.fromstring(html)
    scrapeTable(root)
    sUrl  = "http://jobboerse.arbeitsagentur.de" + root.cssselect(".ergebnisPaginierung a")[2].attrib['href']
scraperwiki.sqlite.commit()

sys.exit()

#cleanup
rows = scraperwiki.sqlite.select("* FROM swdata ORDER BY LENGTH(region) DESC")
print "Starting cleanup of ", len(rows), " rows!"
for record in rows:
    try:    
        for phrase in redundantText:
            record["company"]  = record["company"].replace(phrase, " ").strip()
    except: pass
    try:    
        for phrase in redundantText:
            record["region"]  = record["region"].replace(phrase, " ").strip()
    except: pass
    try:    
        for phrase in redundantText:
            record["name"]  = record["name"].replace(phrase, " ").strip()
    except: pass
    scraperwiki.sqlite.save(["id"], record)