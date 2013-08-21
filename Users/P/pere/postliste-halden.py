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
import urllib
import re
lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Halden kommune'

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

def process_pdf_links_cssselect(parser, listurl, errors, cssselect):
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect(cssselect + " a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "%20").replace(u"å", "%C3%A5")
        #print url
        if -1 != href.find("file://") or -1 != href.find("postliste/Documents/Brukerveiledning"):
#            print "Skipping non-http URL " + url
            continue
        if -1 == href.find(".pdf"):
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def process_journal_pdfs(parser, listurl, errors):
    return process_pdf_links_cssselect(parser, listurl, errors, "div#page_centerElementZone")

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, u"http://www.halden.kommune.no/selvbetjening/postliste/Documents/120601%20-%20120607%20Inng%C3%A5ende.pdf", errors)
    process_pdf(parser, u"http://www.halden.kommune.no/selvbetjening/postliste/Documents/120601%20-%20120607%20Utg%C3%A5ende.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
parser.debug = True

#test_small_pdfs(parser)
process_page_queue(parser, errors)
process_journal_pdfs(parser, u"http://www.halden.kommune.no/selvbetjening/postliste/Sider/Inng%C3%A5ende-postlister.aspx", errors)
process_journal_pdfs(parser, u"http://www.halden.kommune.no/selvbetjening/postliste/Sider/Utg%C3%A5ende-postliste-.aspx", errors)
process_page_queue(parser, errors)
report_errors(errors)