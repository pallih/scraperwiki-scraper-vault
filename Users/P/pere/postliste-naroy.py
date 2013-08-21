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

agency = u'Nærøy kommune'

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
    for ahref in root.cssselect("table#hovedinnhold a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "+")
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if -1 == url.find(".pdf"):
            continue
        # Special case, file indicating no journal entries this day
        if "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/CA6C83764E56DDCBC1257A02003F9025/$FILE/Postjournal+11.05.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/7FD82A18C1A1F137C12579F90029DEBD/$FILE/Postjournal+07.05.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/777B497BB48936ACC1257A450033E1D4/$FILE/Postjournal+20.07.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/1802A0FF57C08EFEC1257A4500337345/$FILE/Postjournal+16.07.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/90373A38701C27E5C1257A45002F63FD/$FILE/Postjournal+12.07.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/6B00A3BD92B3C2AEC1257A45002F4044/$FILE/Postjournal+10.07.12.pdf" == url or \
            "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/0141B5488D38B8FEC1257A44003756ED/$FILE/Postjournal+06.07.12.pdf" == url:
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
    process_pdf(parser, "http://www.naroy.kommune.no/NK/Intern.nsf/FilA/451908E568D2D630C1257A1E004D1B9D/$FILE/Postjournal%2005.06.12.pdf", errors)

    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.naroy.kommune.no/NK/Web.nsf/mainPress?OpenForm&U=POST", errors)
process_page_queue(parser, errors)
report_errors(errors)

