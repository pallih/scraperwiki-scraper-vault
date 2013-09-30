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
lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Storfjord kommune'

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
        parser.fetch_and_preprocess(pdfurl)
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
    for ahref in root.cssselect("div.main a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 == url.find("postliste-"):
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
    process_pdf(parser, "http://www.storfjord.kommune.no/postliste-18-mai-2012.5056067-105358.html", errors)
    process_pdf(parser, "http://www.storfjord.kommune.no/postliste-16-mai-2012.5056059-105358.html", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

parser = postlistelib.PDFJournalParser(agency=agency)
#test_small_pdfs(parser)

errors = []
process_journal_pdfs(parser, "http://www.storfjord.kommune.no/postliste.105358.no.html", errors)
for page in range(2,91):
    process_journal_pdfs(parser, "http://www.storfjord.kommune.no/?cat=105358&apage=" + str(page), errors)
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
lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Storfjord kommune'

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
        parser.fetch_and_preprocess(pdfurl)
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
    for ahref in root.cssselect("div.main a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 == url.find("postliste-"):
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
    process_pdf(parser, "http://www.storfjord.kommune.no/postliste-18-mai-2012.5056067-105358.html", errors)
    process_pdf(parser, "http://www.storfjord.kommune.no/postliste-16-mai-2012.5056059-105358.html", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

parser = postlistelib.PDFJournalParser(agency=agency)
#test_small_pdfs(parser)

errors = []
process_journal_pdfs(parser, "http://www.storfjord.kommune.no/postliste.105358.no.html", errors)
for page in range(2,91):
    process_journal_pdfs(parser, "http://www.storfjord.kommune.no/?cat=105358&apage=" + str(page), errors)
process_page_queue(parser, errors)
report_errors(errors)

