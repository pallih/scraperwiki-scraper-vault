# -*- coding: UTF-8 -*-

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import urlparse
import re

scraperwiki.scrape("http://www.nrk.no/innsyn/")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Norsk Rikskringkasting AS'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise ValueError(str(len(errors)) + " errors detected")

def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

def process_pdf(parser, pdfurl, errors):
    if parser.is_already_scraped(pdfurl):
        return
    postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    try:
        pdfcontent = scraperwiki.scrape(pdfurl)
        parser.preprocess(pdfurl, pdfcontent)
        pdfcontent = None
    except ValueError, e:
        print e
        errors.append(e)
    except IndexError, e:
        print e
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
    xml = scraperwiki.scrape(listurl)
    root = lxml.html.fromstring(xml)
    xml = None
    for link in root.cssselect("hendelse link"):
        url = lxml.html.tostring(link).replace("<link>", "").strip()
        #print url
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            process_pdf(parser, url, errors)

def test_small_pdfs(parser):

    #parser.debug = True

    errors = []

    # 2011:
    if True:
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200101_15012011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200102_10022011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200103_10032011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200104_07042011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200105_05052011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200106_18062011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200107_15072011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200108_15082011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200109_12092011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200110_12102011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200111_10112011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200112_10122011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200605_10052011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200804_15042011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201102_19022011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201103_17032011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201105_20052011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201111_20112011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201112_20122011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201309_25092011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201310_20102011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201601_31012011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201604_30042011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201607_31072011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201608_25082011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201803_26032011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%201906_26062011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202105_31052011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202110_31102011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202111_30112011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202112_31122011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202502_28022011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202608_31082011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202609_30092011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202703_31032011.pdf", errors)
        process_pdf(parser, "http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%202706_30062011.pdf", errors)

    #process_pdf(parser, "http://nrk.no/contentfile/file/1.8116520!offentligjournal02052012.pdf", errors) # text
    #process_pdf(parser, "http://nrk.no/contentfile/file/1.8061384!offentlig%2002042012.pdf", errors) # Image
    #process_pdf(parser, "http://nrk.no/contentfile/file/1.8130287!offentligjournal09052012.pdf", errors) # Image
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency, hiddentext=True)

#test_small_pdfs(parser)

# Based on http://www.nrk.no/innsyn/
process_journal_pdfs(parser, "http://www.nrk.no/contentfile/transformer/1.8052258", errors)
process_page_queue(parser, errors)
report_errors(errors)