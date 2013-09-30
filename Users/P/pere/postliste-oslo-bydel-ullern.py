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
import urlparse
import re

scraperwiki.scrape("http://www.bydel-ullern.oslo.kommune.no/postjournal/")

#lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Oslo kommune, Ullern bydel'

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
    for ahref in root.cssselect("table a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://") or -1 != href.find("mailto:"):
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
    parser.debug = True
    process_pdf(parser, "http://www.bydel-ullern.oslo.kommune.no/getfile.php/bydel%20ullern%20(BUN)/Internett%20(BUN)/Dokumenter/dokument/postjournal/120502.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

print "Starting scraping of " + agency
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

#test_small_pdfs(parser)

errors = []
process_journal_pdfs(parser, "http://www.bydel-ullern.oslo.kommune.no/postjournal/", errors)
process_page_queue(parser, errors)
report_errors(errors)

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
import urlparse
import re

scraperwiki.scrape("http://www.bydel-ullern.oslo.kommune.no/postjournal/")

#lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Oslo kommune, Ullern bydel'

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
    for ahref in root.cssselect("table a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://") or -1 != href.find("mailto:"):
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
    parser.debug = True
    process_pdf(parser, "http://www.bydel-ullern.oslo.kommune.no/getfile.php/bydel%20ullern%20(BUN)/Internett%20(BUN)/Dokumenter/dokument/postjournal/120502.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

print "Starting scraping of " + agency
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

#test_small_pdfs(parser)

errors = []
process_journal_pdfs(parser, "http://www.bydel-ullern.oslo.kommune.no/postjournal/", errors)
process_page_queue(parser, errors)
report_errors(errors)

