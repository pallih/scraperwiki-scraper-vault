# -*- coding: UTF-8 -*-

import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import sys
import urlparse

scraperwiki.scrape("http://www.hadsel.kommune.no/selvbetjeningskjema-kart-postjournal/offentlig-postjournal")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Hadsel kommune'

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
    if parser.is_already_scraped(url):
        True
#            print "Skipping already scraped " + url
    else:
#            print "Will process " + url
        try:
            process_pdf(parser, url, errors)
        except:
            pass

def process_journal_pdfs(parser, listurl, errors, recurse):
#    print "Finding PDFs on " + listurl
#    u = urllib.parse.urlparse(listurl)
    html = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(html)
    html = None
    for ahref in root.cssselect("div.items a"):
        url = urlparse.urljoin(listurl, ahref.attrib['href'])
        if -1 == url.find("doc_download"):
            continue
        consider_url(parser, url, errors)
        #print url
    for ahref in root.cssselect("div.item-list a"):
        suburl = urlparse.urljoin(listurl, ahref.attrib['href'])
        #print "sub " + suburl
        subhtml = scraperwiki.scrape(suburl)
        subroot = lxml.html.fromstring(subhtml)
        subhtml = None
        for subahref in subroot.cssselect("div.article a"):
            href = subahref.attrib['href']
            #print href
            subsuburl = urlparse.urljoin(suburl, href)
            #print "subsub " + subsuburl
            if -1 == subsuburl.find("doc_download"):
                continue
            consider_url(parser, subsuburl, errors)
        subroot = None
    if recurse:
        seen = { listurl : 1 }
        for ahref in root.cssselect("div.pagination a"):
            pageurl = urlparse.urljoin(listurl, ahref.attrib['href'])
            #print "P: " + pageurl
            if pageurl not in seen:
                process_journal_pdfs(parser, pageurl, errors, False)
                seen[pageurl] = 1

def test_parse_case_journal_ref():
    entry = {}
    parse_case_journal_ref(entry, [u'2008/16414-', u'23', u'15060/2012'], "")
    parse_case_journal_ref(entry, [u'2011/15972-1 102773/201', u'1'], "")
    parse_case_journal_ref(entry, [u'2010/2593-2', u'103004/201', u'1'], "")
    parse_case_journal_ref(entry, [u'2011/13415-', u'22', u'100077/201', u'1'], "")
    exit(0)

#test_parse_case_journal_ref()

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)
process_page_queue(parser, errors)
process_journal_pdfs(parser, "http://www.hadsel.kommune.no/selvbetjeningskjema-kart-postjournal/offentlig-postjournal", errors, True)
process_page_queue(parser, errors)
report_errors(errors)

