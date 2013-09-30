# -*- coding: UTF-8 -*-

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import sys
import urlparse

scraperwiki.scrape("http://kristiansund.orkide.acos.no/kunde/web/postliste/postliste.asp")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Kristiansund kommune'
debug = False

def is_already_scraped(url):

    for sql in ["scrapedurl from swdata where scrapedurl = '" + url + "' limit 1",
                "scrapedurl from unparsedpages where scrapedurl = '" + url + "' limit 1"]:
#    print sql
        try:
            result = scraperwiki.sqlite.select(sql)
#    print result
            if 0 < len(result) and u'scrapedurl' in result[0]:
                return True
        except:
            pass
    return False

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)
def no_cpu_left(arg, spent, soft, hard):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    errors = []
    postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    try:
        pdfcontent = lazycache.lazycache(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
#    except ValueError, e:
#        errors.append(e)
    except IndexError, e:
        errors.append(e)

def process_page_queue(parser, errors):
    try:
        parser.process_pages()
        postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    except scraperwiki.CPUTimeExceededError, e:
        errors.append("Processing pages interrupted")

def consider_url(parser, url, errors):
    if is_already_scraped(url):
        True
#            print "Skipping already scraped " + url
    else:
#            print "Will process " + url
        process_pdf(parser, url, errors)

def process_journal_pdfs(parser, listurl, errors):
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("table a"):
        url = urlparse.urljoin(listurl, ahref.attrib['href'])
        if -1 == url.find(".pdf"):
            continue
        consider_url(parser, url, errors)

#test_parse_case_journal_ref()
errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True
process_journal_pdfs(parser, "http://kristiansund.orkide.acos.no/kunde/web/postliste/postliste.asp", errors)
process_page_queue(parser, errors)
report_errors(errors)

# -*- coding: UTF-8 -*-

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import sys
import urlparse

scraperwiki.scrape("http://kristiansund.orkide.acos.no/kunde/web/postliste/postliste.asp")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Kristiansund kommune'
debug = False

def is_already_scraped(url):

    for sql in ["scrapedurl from swdata where scrapedurl = '" + url + "' limit 1",
                "scrapedurl from unparsedpages where scrapedurl = '" + url + "' limit 1"]:
#    print sql
        try:
            result = scraperwiki.sqlite.select(sql)
#    print result
            if 0 < len(result) and u'scrapedurl' in result[0]:
                return True
        except:
            pass
    return False

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)
def no_cpu_left(arg, spent, soft, hard):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    errors = []
    postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    try:
        pdfcontent = lazycache.lazycache(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
#    except ValueError, e:
#        errors.append(e)
    except IndexError, e:
        errors.append(e)

def process_page_queue(parser, errors):
    try:
        parser.process_pages()
        postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    except scraperwiki.CPUTimeExceededError, e:
        errors.append("Processing pages interrupted")

def consider_url(parser, url, errors):
    if is_already_scraped(url):
        True
#            print "Skipping already scraped " + url
    else:
#            print "Will process " + url
        process_pdf(parser, url, errors)

def process_journal_pdfs(parser, listurl, errors):
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("table a"):
        url = urlparse.urljoin(listurl, ahref.attrib['href'])
        if -1 == url.find(".pdf"):
            continue
        consider_url(parser, url, errors)

#test_parse_case_journal_ref()
errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True
process_journal_pdfs(parser, "http://kristiansund.orkide.acos.no/kunde/web/postliste/postliste.asp", errors)
process_page_queue(parser, errors)
report_errors(errors)

