# -*- coding: UTF-8 -*-

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

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.hivolda.no/nyn/hivolda/om-hogskulen/administrasjon/dokumentsenteret")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Volda'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise ValueError("Something went wrong")

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
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div#maincontent a"):
        if 'id' not in ahref.attrib or -1 == ahref.attrib['id'].find("archiveimage_"):
            continue
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        #print "found url %s" %url
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.hivolda.no/neted/modules/archive/front/file.php?data=47449f5f5477b30f13f282759d5f08b1", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.hivolda.no/nyn/hivolda/om-hogskulen/administrasjon/dokumentsenteret", errors)
process_page_queue(parser, errors)
report_errors(errors)

# -*- coding: UTF-8 -*-

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

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.hivolda.no/nyn/hivolda/om-hogskulen/administrasjon/dokumentsenteret")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Volda'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise ValueError("Something went wrong")

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
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div#maincontent a"):
        if 'id' not in ahref.attrib or -1 == ahref.attrib['id'].find("archiveimage_"):
            continue
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        #print "found url %s" %url
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.hivolda.no/neted/modules/archive/front/file.php?data=47449f5f5477b30f13f282759d5f08b1", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.hivolda.no/nyn/hivolda/om-hogskulen/administrasjon/dokumentsenteret", errors)
process_page_queue(parser, errors)
report_errors(errors)

