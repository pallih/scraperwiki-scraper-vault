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
import urllib2, base64

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.hiof.no/nor/hogskolen-i-ostfold/om-hogskolen/administrasjonen/arkivet/offentlig-journal")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Østfold'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)

def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
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
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div.text_content table tr td a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "+")
        if (-1 == url.find("mnd.pdf")) and (-1 == url.find("dag.pdf")):
            continue

        # We get the ETag since the url does not change
        request = urllib2.Request(url)
        request.get_method = lambda : 'HEAD'
        response = urllib2.urlopen(request)
        #print response.info()
        etag = base64.b64encode(response.info().getheader("ETag"))
        url = "%s#%s" % (url, etag) # Yes, the etag is surrounded by ""
        if parser.is_already_scraped(url):
            continue
        else:
            print "Prosessing %s" % url
            process_pdf(parser, url, errors)


errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
process_journal_pdfs(parser, "http://www.hiof.no/nor/hogskolen-i-ostfold/om-hogskolen/administrasjonen/arkivet/offentlig-journal", errors)
process_page_queue(parser, errors)
report_errors(errors)

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
import urllib2, base64

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.hiof.no/nor/hogskolen-i-ostfold/om-hogskolen/administrasjonen/arkivet/offentlig-journal")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Høgskolen i Østfold'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)

def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
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
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div.text_content table tr td a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href).replace(" ", "+")
        if (-1 == url.find("mnd.pdf")) and (-1 == url.find("dag.pdf")):
            continue

        # We get the ETag since the url does not change
        request = urllib2.Request(url)
        request.get_method = lambda : 'HEAD'
        response = urllib2.urlopen(request)
        #print response.info()
        etag = base64.b64encode(response.info().getheader("ETag"))
        url = "%s#%s" % (url, etag) # Yes, the etag is surrounded by ""
        if parser.is_already_scraped(url):
            continue
        else:
            print "Prosessing %s" % url
            process_pdf(parser, url, errors)


errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
process_journal_pdfs(parser, "http://www.hiof.no/nor/hogskolen-i-ostfold/om-hogskolen/administrasjonen/arkivet/offentlig-journal", errors)
process_page_queue(parser, errors)
report_errors(errors)

