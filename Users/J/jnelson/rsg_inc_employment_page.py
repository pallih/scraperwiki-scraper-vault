import scraperwiki         
import lxml.html
from urlparse import urlparse, parse_qs # becomes urllib.parse @ Python v3
import datetime
import urllib2

html = scraperwiki.scrape("http://www.rsginc.com/home/employment/")
root = lxml.html.fromstring(html)
date = datetime.datetime.now()
dbid = 'rsg_inc_employment_page'
scraperwiki.sqlite.attach(dbid)

for el in root.cssselect("div.job a"):
    joblink = "http://www.rsginc.com" + el.attrib['href']
    jobhtml = scraperwiki.scrape(joblink)
    jobroot = lxml.html.fromstring(jobhtml)
    jobel = jobroot.cssselect("div.job")[0]
    applink = jobel.cssselect("h3 a")[0].attrib['href']
    #print applink
    appkey = parse_qs( urlparse(applink).query )['id'][0]
    #print appkey
    try:
        prior = scraperwiki.sqlite.select("* FROM "+dbid+".swdata WHERE appkey ='"+appkey+"'")
        print "prior records exist"
    except:
        print "no prior records found"
        prior = []
    if len(prior)==0:
        position = jobel.cssselect("h3.cgtrade")[0].text
        #print position
        location = jobel.cssselect("h4")[0].text
        #print location
        detail_html = ""
        for det in jobel.cssselect("p,ul"):
            detail_html += lxml.html.tostring(det) + "\n"
        #print detail_html
        record = { "appkey":appkey, "joblink":joblink, "date":date, "applink":applink, "position":position, "location":location, "detail_html":detail_html }
        scraperwiki.sqlite.save(unique_keys=['appkey'], data=record)
    else:
        #puts "Skipping already saved record " + record['joblink']
        print "Skipping already saved record for URL=" + joblink
import scraperwiki         
import lxml.html
from urlparse import urlparse, parse_qs # becomes urllib.parse @ Python v3
import datetime
import urllib2

html = scraperwiki.scrape("http://www.rsginc.com/home/employment/")
root = lxml.html.fromstring(html)
date = datetime.datetime.now()
dbid = 'rsg_inc_employment_page'
scraperwiki.sqlite.attach(dbid)

for el in root.cssselect("div.job a"):
    joblink = "http://www.rsginc.com" + el.attrib['href']
    jobhtml = scraperwiki.scrape(joblink)
    jobroot = lxml.html.fromstring(jobhtml)
    jobel = jobroot.cssselect("div.job")[0]
    applink = jobel.cssselect("h3 a")[0].attrib['href']
    #print applink
    appkey = parse_qs( urlparse(applink).query )['id'][0]
    #print appkey
    try:
        prior = scraperwiki.sqlite.select("* FROM "+dbid+".swdata WHERE appkey ='"+appkey+"'")
        print "prior records exist"
    except:
        print "no prior records found"
        prior = []
    if len(prior)==0:
        position = jobel.cssselect("h3.cgtrade")[0].text
        #print position
        location = jobel.cssselect("h4")[0].text
        #print location
        detail_html = ""
        for det in jobel.cssselect("p,ul"):
            detail_html += lxml.html.tostring(det) + "\n"
        #print detail_html
        record = { "appkey":appkey, "joblink":joblink, "date":date, "applink":applink, "position":position, "location":location, "detail_html":detail_html }
        scraperwiki.sqlite.save(unique_keys=['appkey'], data=record)
    else:
        #puts "Skipping already saved record " + record['joblink']
        print "Skipping already saved record for URL=" + joblink
