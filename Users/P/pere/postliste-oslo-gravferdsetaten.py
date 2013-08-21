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

scraperwiki.scrape("http://www.gravferdsetaten.oslo.kommune.no/offentlig_journal/article43281-14384.html")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Oslo kommune, gravferdsetaten'

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
        if False:
            scraperwiki.sqlite.execute("delete from swdata where scrapedurl in (select scrapedurl from unparsedpages)")
            scraperwiki.sqlite.execute("delete from unparsedpages")
            scraperwiki.sqlite.commit()

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
    process_pdf(parser, "http://www.gravferdsetaten.oslo.kommune.no/getfile.php/gravferdsetaten%20(GFE)/Internett%20(GFE)/Dokumenter/dokument/Arkivet/Postjournal/Juni/13.06.pdf", errors)
    process_pdf(parser, "http://www.gravferdsetaten.oslo.kommune.no/getfile.php/gravferdsetaten%20(GFE)/Internett%20(GFE)/Dokumenter/dokument/Arkivet/Postjournal/Juni/12.06.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.gravferdsetaten.oslo.kommune.no/offentlig_journal/article43281-14384.html", errors)
process_page_queue(parser, errors)
report_errors(errors)

