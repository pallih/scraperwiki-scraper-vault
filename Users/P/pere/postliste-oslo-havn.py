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
import sys
import urlparse
import re

scraperwiki.scrape("http://www.havn.oslo.kommune.no/postjournal/")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Oslo kommune, Oslo Havn KF'

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
        parser.fetch_and_preprocess(pdfurl)
    except ValueError, e:
        errors.append(e)
    except IndexError, e:
        errors.append(e)

def process_page_queue(parser, errors):
    try:
        parser.process_pages()
        postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    except scraperwiki.CPUTimeExceededError, e:
        errors.append("Processing pages interrupted, ran out of cpu")

def process_journal_pdfs(parser, listurl, errors):
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("table a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def test_pdfs(parser):
    parser.debug = True
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.havn.oslo.kommune.no/getfile.php/oslo%20havn%20kf%20(HAV)/Internett%20(HAV)/Dokumenter/Postjournal/Mai/24.05.2012.pdf", errors)

    # This file have a problematic format, the text fragments have a different order than most
    # journal PDFs.
    process_pdf(parser, "http://www.havn.oslo.kommune.no/getfile.php/oslo%20havn%20kf%20%28HAV%29/Internett%20%28HAV%29/Dokumenter/Postjournal/Mars/1%20MTMzMDY4NjY3ODI5OTk5Mz.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

parser = postlistelib.PDFJournalParser(agency=agency)

#test_pdfs(parser)

errors = []
process_journal_pdfs(parser, "http://www.havn.oslo.kommune.no/postjournal/", errors)
process_page_queue(parser, errors)
report_errors(errors)

