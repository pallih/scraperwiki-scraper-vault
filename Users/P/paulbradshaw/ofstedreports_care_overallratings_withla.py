#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"

record = {}

def scrapereport(reportlink):
    boldline = 0
    html = scraperwiki.scrape(baseurl+reportlink)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#unusefulbottom a")
    #<div id="unusefulbottom">
    for link in links:
        print "LINK GRABBED WITH CSSSELECT", link
        print "link.attrib.get", link.attrib.get('href')
        downloadlink = link.attrib.get('href')
#    print " downloadlink[0].text_content()", downloadlink[0].text_content()
        pdfdata = urllib2.urlopen(baseurl+downloadlink).read()
        print "pdfdata", pdfdata
        xmldata = scraperwiki.pdftoxml(pdfdata)
        print "xmldata", xmldata
        pdfxml = lxml.etree.fromstring(xmldata)
        print "pdfxml", pdfxml
        boldtags = pdfxml.xpath('.//text')
        linenumber = 0
        for heading in boldtags:
            linenumber = linenumber+1
            #print "Heading:", heading.text
            if heading.text is not None:
#                mention = re.match(r'.*NMS.*',heading.text)
                mention = re.match(r'.*overall.*',heading.text)
                if mention:
                    print "FULL LINE", lxml.etree.tostring(heading, encoding="unicode", method="text")
#                    print "OVERALL", heading.text
#                    print "CHECK", pdfxml.xpath('.//text')[linenumber-1].text
#                    print "LINEAFTER", pdfxml.xpath('.//text')[linenumber].text
                    record['overall'] = lxml.etree.tostring(heading, encoding="unicode", method="text")
                    record['uniqueref'] = reportlink+"_"+str(boldline)
                    record['downloadlink'] = baseurl+downloadlink
                    scraperwiki.sqlite.save(['uniqueref'],record)

def scrapelinks(url):
    print "GRABBING PARTIAL LINKS FROM:", url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("tr td")
    for row in rows:
        reportlink = row.text_content()
        print "ABOUT TO SCRAPE:", reportlink
        scrapereport(reportlink)

#This shows all the report URLs from the previous scraper
linksurl = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=inspectionreportschildrenshomes&query=select%20report1url%20from%20%60swdata%60%20'

#START HERE
scrapelinks(linksurl)

#this thread on stackoverflow used to grab <b> tags inside ratings line: 
#http://stackoverflow.com/questions/4770191/lxml-etree-element-text-doesnt-return-the-entire-text-from-an-element

#for this error: 'ascii' codec can't encode character u'\u2019' in position 70: ordinal not in range(128)
#added encoding="unicode", to two lines#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"

record = {}

def scrapereport(reportlink):
    boldline = 0
    html = scraperwiki.scrape(baseurl+reportlink)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#unusefulbottom a")
    #<div id="unusefulbottom">
    for link in links:
        print "LINK GRABBED WITH CSSSELECT", link
        print "link.attrib.get", link.attrib.get('href')
        downloadlink = link.attrib.get('href')
#    print " downloadlink[0].text_content()", downloadlink[0].text_content()
        pdfdata = urllib2.urlopen(baseurl+downloadlink).read()
        print "pdfdata", pdfdata
        xmldata = scraperwiki.pdftoxml(pdfdata)
        print "xmldata", xmldata
        pdfxml = lxml.etree.fromstring(xmldata)
        print "pdfxml", pdfxml
        boldtags = pdfxml.xpath('.//text')
        linenumber = 0
        for heading in boldtags:
            linenumber = linenumber+1
            #print "Heading:", heading.text
            if heading.text is not None:
#                mention = re.match(r'.*NMS.*',heading.text)
                mention = re.match(r'.*overall.*',heading.text)
                if mention:
                    print "FULL LINE", lxml.etree.tostring(heading, encoding="unicode", method="text")
#                    print "OVERALL", heading.text
#                    print "CHECK", pdfxml.xpath('.//text')[linenumber-1].text
#                    print "LINEAFTER", pdfxml.xpath('.//text')[linenumber].text
                    record['overall'] = lxml.etree.tostring(heading, encoding="unicode", method="text")
                    record['uniqueref'] = reportlink+"_"+str(boldline)
                    record['downloadlink'] = baseurl+downloadlink
                    scraperwiki.sqlite.save(['uniqueref'],record)

def scrapelinks(url):
    print "GRABBING PARTIAL LINKS FROM:", url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("tr td")
    for row in rows:
        reportlink = row.text_content()
        print "ABOUT TO SCRAPE:", reportlink
        scrapereport(reportlink)

#This shows all the report URLs from the previous scraper
linksurl = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=inspectionreportschildrenshomes&query=select%20report1url%20from%20%60swdata%60%20'

#START HERE
scrapelinks(linksurl)

#this thread on stackoverflow used to grab <b> tags inside ratings line: 
#http://stackoverflow.com/questions/4770191/lxml-etree-element-text-doesnt-return-the-entire-text-from-an-element

#for this error: 'ascii' codec can't encode character u'\u2019' in position 70: ordinal not in range(128)
#added encoding="unicode", to two lines#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"

record = {}

def scrapereport(reportlink):
    boldline = 0
    html = scraperwiki.scrape(baseurl+reportlink)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#unusefulbottom a")
    #<div id="unusefulbottom">
    for link in links:
        print "LINK GRABBED WITH CSSSELECT", link
        print "link.attrib.get", link.attrib.get('href')
        downloadlink = link.attrib.get('href')
#    print " downloadlink[0].text_content()", downloadlink[0].text_content()
        pdfdata = urllib2.urlopen(baseurl+downloadlink).read()
        print "pdfdata", pdfdata
        xmldata = scraperwiki.pdftoxml(pdfdata)
        print "xmldata", xmldata
        pdfxml = lxml.etree.fromstring(xmldata)
        print "pdfxml", pdfxml
        boldtags = pdfxml.xpath('.//text')
        linenumber = 0
        for heading in boldtags:
            linenumber = linenumber+1
            #print "Heading:", heading.text
            if heading.text is not None:
#                mention = re.match(r'.*NMS.*',heading.text)
                mention = re.match(r'.*overall.*',heading.text)
                if mention:
                    print "FULL LINE", lxml.etree.tostring(heading, encoding="unicode", method="text")
#                    print "OVERALL", heading.text
#                    print "CHECK", pdfxml.xpath('.//text')[linenumber-1].text
#                    print "LINEAFTER", pdfxml.xpath('.//text')[linenumber].text
                    record['overall'] = lxml.etree.tostring(heading, encoding="unicode", method="text")
                    record['uniqueref'] = reportlink+"_"+str(boldline)
                    record['downloadlink'] = baseurl+downloadlink
                    scraperwiki.sqlite.save(['uniqueref'],record)

def scrapelinks(url):
    print "GRABBING PARTIAL LINKS FROM:", url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("tr td")
    for row in rows:
        reportlink = row.text_content()
        print "ABOUT TO SCRAPE:", reportlink
        scrapereport(reportlink)

#This shows all the report URLs from the previous scraper
linksurl = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=inspectionreportschildrenshomes&query=select%20report1url%20from%20%60swdata%60%20'

#START HERE
scrapelinks(linksurl)

#this thread on stackoverflow used to grab <b> tags inside ratings line: 
#http://stackoverflow.com/questions/4770191/lxml-etree-element-text-doesnt-return-the-entire-text-from-an-element

#for this error: 'ascii' codec can't encode character u'\u2019' in position 70: ordinal not in range(128)
#added encoding="unicode", to two lines#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"

record = {}

def scrapereport(reportlink):
    boldline = 0
    html = scraperwiki.scrape(baseurl+reportlink)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div#unusefulbottom a")
    #<div id="unusefulbottom">
    for link in links:
        print "LINK GRABBED WITH CSSSELECT", link
        print "link.attrib.get", link.attrib.get('href')
        downloadlink = link.attrib.get('href')
#    print " downloadlink[0].text_content()", downloadlink[0].text_content()
        pdfdata = urllib2.urlopen(baseurl+downloadlink).read()
        print "pdfdata", pdfdata
        xmldata = scraperwiki.pdftoxml(pdfdata)
        print "xmldata", xmldata
        pdfxml = lxml.etree.fromstring(xmldata)
        print "pdfxml", pdfxml
        boldtags = pdfxml.xpath('.//text')
        linenumber = 0
        for heading in boldtags:
            linenumber = linenumber+1
            #print "Heading:", heading.text
            if heading.text is not None:
#                mention = re.match(r'.*NMS.*',heading.text)
                mention = re.match(r'.*overall.*',heading.text)
                if mention:
                    print "FULL LINE", lxml.etree.tostring(heading, encoding="unicode", method="text")
#                    print "OVERALL", heading.text
#                    print "CHECK", pdfxml.xpath('.//text')[linenumber-1].text
#                    print "LINEAFTER", pdfxml.xpath('.//text')[linenumber].text
                    record['overall'] = lxml.etree.tostring(heading, encoding="unicode", method="text")
                    record['uniqueref'] = reportlink+"_"+str(boldline)
                    record['downloadlink'] = baseurl+downloadlink
                    scraperwiki.sqlite.save(['uniqueref'],record)

def scrapelinks(url):
    print "GRABBING PARTIAL LINKS FROM:", url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("tr td")
    for row in rows:
        reportlink = row.text_content()
        print "ABOUT TO SCRAPE:", reportlink
        scrapereport(reportlink)

#This shows all the report URLs from the previous scraper
linksurl = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=inspectionreportschildrenshomes&query=select%20report1url%20from%20%60swdata%60%20'

#START HERE
scrapelinks(linksurl)

#this thread on stackoverflow used to grab <b> tags inside ratings line: 
#http://stackoverflow.com/questions/4770191/lxml-etree-element-text-doesnt-return-the-entire-text-from-an-element

#for this error: 'ascii' codec can't encode character u'\u2019' in position 70: ordinal not in range(128)
#added encoding="unicode", to two lines