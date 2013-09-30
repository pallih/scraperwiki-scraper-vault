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

# Load front page first, to get it recorded as the source by scraperwiki
scraperwiki.scrape("http://www.npolar.no/no/om-oss/offentlig-journal.html")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Norsk Polarinstitutt'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)
def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    errors = []
    postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    try:
        pdfcontent = scraperwiki.scrape(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
        pdfcontent = None
#    except ValueError, e:
#        errors.append(e)
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
    for ahref in root.cssselect("div.onecol ul a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://") or -1 == url.find(".pdf"):
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
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-10.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-09.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-08.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-07.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-06.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-05.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-04.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-03.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-02.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-01.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournalapril-mai2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljanuar-mai2011.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljanuar-mars2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljuni-oktober2011.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljuni2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournalnovember-desember2011.pdf", errors)

    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.npolar.no/no/om-oss/offentlig-journal.html", errors)
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

# Load front page first, to get it recorded as the source by scraperwiki
scraperwiki.scrape("http://www.npolar.no/no/om-oss/offentlig-journal.html")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Norsk Polarinstitutt'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)
def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    errors = []
    postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    try:
        pdfcontent = scraperwiki.scrape(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
        pdfcontent = None
#    except ValueError, e:
#        errors.append(e)
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
    for ahref in root.cssselect("div.onecol ul a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://") or -1 == url.find(".pdf"):
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
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-10.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-09.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-08.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-07.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-06.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-05.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-04.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-03.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-02.pdf", errors)
    #process_pdf(parser, "http://www.npolar.no/npcms/export/sites/np/files/vedlegg/offentlig-journal/2011-01.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournalapril-mai2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljanuar-mai2011.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljanuar-mars2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljuni-oktober2011.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournaljuni2012.pdf", errors)
    process_pdf(parser, "http://home.nuug.no/~pere/npolar-postjournal/OffJournalnovember-desember2011.pdf", errors)

    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.npolar.no/no/om-oss/offentlig-journal.html", errors)
process_page_queue(parser, errors)
report_errors(errors)

