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
lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Universitetet i Stavanger'

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
    for ahref in root.cssselect("div#placeholder-content-main-left-column a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://") or -1 == url.find('/postjournal/article'):
#            print "Skipping non-http URL " + url
            continue
        subhtml = scraperwiki.scrape(url)
        subroot = lxml.html.fromstring(subhtml)
        subhtml = None
        for subahref in subroot.cssselect("div.article-content a"):
            subhref = subahref.attrib['href']
            suburl = urlparse.urljoin(listurl, subhref)
            if -1 == suburl.find(".pdf"):
                continue
            if parser.is_already_scraped(suburl):
                True
#            print "Skipping already scraped " + suburl
            else:
#                print "Will process " + suburl
                process_pdf(parser, suburl, errors)

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.uis.no/getfile.php/Journal%20200612.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.uis.no/nyheter/postjournal/", errors)
process_page_queue(parser, errors)
report_errors(errors)

