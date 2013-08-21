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
scraperwiki.scrape("http://www.hihm.no/Hovedsiden/Om-Hoegskolen/Offentlig-journal")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Hedmark'

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
    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div.content-view-full a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "+")
        if -1 != href.find("file://") or -1 == url.find(".pdf"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def find_journal_subpages(baseurl):
    urls = []    
    root = lxml.html.fromstring(scraperwiki.scrape(baseurl))
    for ahref in root.cssselect("ul.menu-list a"):
        href = ahref.attrib['href']
        months = "januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"
        if -1 == href.find("file://") and href.endswith(months):
            urls.append(urlparse.urljoin(baseurl, href).replace(" ", "+"))
    return urls

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.hihm.no/content/download/38169/420508/file/search.pdf", errors)
    process_pdf(parser, "http://www.hihm.no/content/download/39369/430053/file/search.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

#process_journal_pdfs(parser, "http://www.hihm.no/Hovedsiden/Om-Hoegskolen/Offentlig-journal/mai", errors)

for url in find_journal_subpages("http://www.hihm.no/Hovedsiden/Om-Hoegskolen/Offentlig-journal"):
    process_journal_pdfs(parser, url, errors)

process_page_queue(parser, errors)
report_errors(errors)

