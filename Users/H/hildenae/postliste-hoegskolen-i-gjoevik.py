# -*- coding: UTF-8 -*-
# Based on the scraper advanced-scraping-pdf
# See also
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/?url=http%3A%2F%2Fwww.stortinget.no%2FGlobal%2Fpdf%2Fpostjournal%2Fpj-2012-05-09.pdf

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import resource
import sys
import urlparse
import re
#
#  something weird with 04.11.2010
#
#
#
# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.hig.no/om_hig/offentleg_journal")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Gjøvik'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise ValueError(str(len(errors)) + " errors detected")

def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    try:
        pdfcontent = scraperwiki.scrape(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
        pdfcontent = None
    except ValueError, e:
        errors.append(e)
    except IndexError, e:
        errors.append(e)

def process_page_queue(parser, errors):
    try:
        parser.process_pages()
        postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    except scraperwiki.CPUTimeExceededError, e:
        errors.append("Processing pages interrupted")

def process_journal_pdfs(parser, listurl, errors):
    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("section a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "+")
        #print url
        if -1 != href.find("file://") or -1 == url.find(".pdf"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            #print "Scraped: %s" % url
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

#def test_small_pdfs(parser):
    # Test with some smaller PDFs
#    errors = []
#    if parser.is_already_scraped("http://www.hig.no/content/download/30119/360872/file/Offentlig+journal+04.11.2010.pdf"):
#        print "Skipping already scraped "
#        exit(1)
#    else:
#        print "Will process "
    #process_pdf(parser, "http://www.hig.no/content/download/35184/430061/file/Offentlig%20journal%2025.06.2012.pdf", errors)
    #process_pdf(parser, "http://www.hig.no/content/download/30116/360863/file/Offentlig%20journal%2001.11.2010.pdf", errors)
#    process_pdf(parser, "http://www.hig.no/content/download/30119/360872/file/Offentlig+journal+04.11.2010.pdf", errors)
#    process_page_queue(parser, errors)
#    report_errors(errors)
#    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

startYear=2010
endYear=datetime.datetime.now().year

for year in range(startYear, endYear+1): # range goes from startyear to endYear-1
    process_journal_pdfs(parser, "http://www.hig.no/om_hig/offentleg_journal/%d" % year, errors)

process_page_queue(parser, errors)
report_errors(errors)

warningQuery = "recorddate as lastupdate from 'swdata' order by recorddate DESC limit 1";
result = scraperwiki.sqlite.select(warningQuery)
now=datetime.datetime.today()
then=datetime.datetime.strptime(result[0]['lastupdate'],"20%y-%m-%dT%H:%M:%S")

if (now-then).days > 14:
    print "warning"
    warningURL = "http://hild1.no/~hildenae/files/dynamic/run.php?scraper=postliste-hoegskolen-i-gjoevik&reason=7days";
    scraperwiki.scrape(warningURL)