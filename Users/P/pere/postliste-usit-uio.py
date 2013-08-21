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

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.uio.no/om/journal/")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'USIT, Universitetet i Oslo'

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
        if -1 != href.find("file://") or -1 == url.find(".pdf"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def process_journal_pdf_directory(parser, listurl, errors):
    #html = scraperwiki.scrape(listurl)
    html = lazycache.lazycache(listurl)
    root = lxml.html.fromstring(html)
    html = None

    pdflisturls = []
    for ahref in root.cssselect("span.vrtx-paging-wrapper a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        pdflisturls.append(url)
#    print pdflisturls

    for listurl in pdflisturls:
        html = scraperwiki.scrape(listurl)
        root = lxml.html.fromstring(html)
        html = None
        urlseen = {}
        for ahref in root.cssselect("div.vrtx-resource a"):
            href = ahref.attrib['href']
            url = urlparse.urljoin(listurl, href)
            if -1 == url.find(".pdf"):
                continue
            # Ignore duplicates with M: as part of the name
            if -1 != url.find("/M%"):
                continue
            if url in urlseen or parser.is_already_scraped(url):
                True
#                print "Skipping already scraped " + url
            else:
#                print "Will process " + url
                process_pdf(parser, url, errors)
            urlseen[url] = 1

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
#    process_pdf(parser, "http://www.nuug.no/pub/offentliginnsyn/from-USIT-UiO/Journalposter%202008.pdf", errors)
#    process_pdf(parser, "http://www.nuug.no/pub/offentliginnsyn/from-USIT-UiO/Journalposter%202009.pdf", errors)
#    process_pdf(parser, "http://www.nuug.no/pub/offentliginnsyn/from-USIT-UiO/Journalposter%202010.pdf", errors)

    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

test_small_pdfs(parser)

#process_journal_pdfs(parser, "http://www.uio.no/om/journal/", errors)
#process_journal_pdf_directory(parser, "http://www.uio.no/om/journal/2012/", errors)
#process_journal_pdf_directory(parser, "http://www.uio.no/om/journal/2011/", errors)
process_page_queue(parser, errors)
report_errors(errors)

