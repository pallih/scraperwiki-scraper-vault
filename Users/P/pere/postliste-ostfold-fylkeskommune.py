# -*- coding: UTF-8 -*-

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import urlparse
import re
import httplib, urllib

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.ostfold-f.kommune.no/offjournal_show_index.asp?m=1388")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Østfold fylkeskommune'

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
#http://www.ostfold-f.kommune.no/offjournal_show_index.asp?tmpSearch=1
    for week in range(1,53):
        params = urllib.urlencode({'tmpSearch' : str(week), 'btnSubmit' : 'Vis', 'strHandling' : 'uke'})

        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"}
        conn = httplib.HTTPConnection("www.ostfold-f.kommune.no:80")
        conn.request("POST", "/offjournal_show_index.asp", params, headers)
        response = conn.getresponse()
        html = response.read()
        conn.close()
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

def test_small_pdfs(parser):
    # Test with some smaller PDFs
    errors = []
    process_pdf(parser, "http://www.ostfold-f.kommune.no/upload%5Coffentligjournal%5C12-12-11man.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.ostfold-f.kommune.no/offjournal_show_index.asp?m=1388", errors)
process_page_queue(parser, errors)
report_errors(errors)

