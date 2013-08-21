# -*- coding: UTF-8 -*-

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import urlparse
import re

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/postjournal/")

lazycache=scraperwiki.swimport('lazycache')
postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Oslo kommune, Rådhusets forvaltningstjeneste'

def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        exit(1)

def out_of_cpu(arg, spent, hard, soft):
    report_errors(arg)

# Input YY/X-Z, return YYYY, X, Z
def split_docid(docid):
    caseyear, rest = docid.split('/')
    caseseqnr, casedocseq = rest.split('-')
    caseyear = int(caseyear)
    caseseqnr = int(caseseqnr)
    casedocsec = int(casedocseq)
    if caseyear < 50:
        caseyear = caseyear + 2000
    if 50 <= caseyear and caseyear < 100:
        caseyear = caseyear + 1900
    return caseyear, caseseqnr, casedocseq

# Input DDMMYYYY, output YYYY-MM-DD
def parse_date(date):
    if 'Udatert' == date:
        return None
    year = date[4:8]
    month = date[2:4]
    day = date[0:2]
    isodate = year + "-" + month + "-" + day
    #print date, isodate
    return dateutil.parser.parse(isodate, dayfirst=True).date()

def parse_entry(pdfurl, lines):
    print lines
    print "Entry lines " + str(len(lines))
    entry = {
        'agency' : agency,
        'scrapedurl' : pdfurl,
    }
    cur = 0
    while cur < len(lines):
        line = lines[cur].text
            #print line
        if -1 != line.find('Dok.dato:'):
            entry['docid'] = lines[cur-2].text
            entry['doctype'] = lines[cur-1].text
            entry['docdate'] = parse_date(line.replace("Dok.dato:", ""))
            caseyear, caseseqnr, casedocseq = split_docid(entry['docid'])
            entry['caseyear'] = caseyear
            entry['caseseqnr'] = caseseqnr
            entry['casedocseq'] = casedocseq
            entry['caseid'] = str(caseyear) + '/' + str(caseseqnr)
        if -1 != line.find('Jour.dato:'):
            entry['recorddate'] = parse_date(lines[cur+1].text)
            cur = cur + 1
        if -1 != line.find('Arkivdel:'):
            entry['arkivdel'] = lines[cur+1].text
            cur = cur + 1
        if -1 != line.find('Tilg. kode:'):
            entry['tilgangskode'] = line.replace("Tilg. kode:", "")
        if -1 != line.find('Sak:'):
            entry['casedesc'] = lines[cur+1].text
            cur = cur + 1
        if -1 != line.find('Dok:'):
            entry['docdesc'] = lines[cur+1].text
            cur = cur + 1
        if -1 != line.find('Par.:'):
            entry['exemption'] = line.replace("Par.:", "")
            cur = cur + 1
        if -1 != line.find('Avsender:'):
            entry['sender'] = lines[cur+1].text
            cur = cur + 1
        if -1 != line.find('Mottaker:'):
            entry['recipient'] = lines[cur+1].text
            cur = cur + 1
        if -1 != line.find('Saksansv:'):
            entry['saksansvarlig'] = line.replace("Saksansv:", "").strip()
        if -1 != line.find('Saksbeh:'):
            entry['saksbehandler'] = lines[cur+1].text
            cur = cur + 1
        cur = cur + 1
    print entry
    if 'docid' in entry:
        scraperwiki.sqlite.save(unique_keys=['docid'], data=entry)
    #return

def parse_pdf(pdfurl, pdfcontent):
    pdfxml = scraperwiki.pdftoxml(pdfcontent)
    pages=re.findall('(<page .+?</page>)',pdfxml,flags=re.DOTALL)
    for page in pages:
        s = BeautifulSoup(page)
        lines = s.findAll('text')
        last = 0
        cur = 0
        while cur < len(lines):
            #print cur, lines[cur]
            if -1 != lines[cur].text.find('Dok.dato:'):
                print last, cur-2
                parse_entry(pdfurl, lines[last:cur-2])
                last = cur - 2
            cur = cur + 1
    return
    if False:
        cur = 0
        entry = { 'agency' : agency, 'scrapedurl' : pdfurl }
        while cur < len(lines):
            line = lines[cur].text
            #print line
            if -1 != line.find('Dok.dato:'):
                entry['docid'] = lines[cur-2].text
                entry['doctype'] = lines[cur-1].text
                entry['docdate'] = parse_date(line.replace("Dok.dato:", ""))
                caseyear, caseseqnr, casedocseq = split_docid(entry['docid'])
                entry['caseyear'] = caseyear
                entry['caseseqnr'] = caseseqnr
                entry['casedocseq'] = casedocseq
                entry['caseid'] = str(caseyear) + '/' + str(caseseqnr)
            if -1 != line.find('Jour.dato:'):
                entry['recorddate'] = parse_date(lines[cur+1].text)
                cur = cur + 1
            if -1 != line.find('Arkivdel:'):
                entry['arkivdel'] = lines[cur+1].text
                cur = cur + 1
            if -1 != line.find('Tilg. kode:'):
                entry['tilgangskode'] = line.replace("Tilg. kode:", "")
            if -1 != line.find('Sak:'):
                entry['casedesc'] = lines[cur+1].text
                cur = cur + 1
            if -1 != line.find('Dok:'):
                entry['docdesc'] = lines[cur+1].text
                cur = cur + 1
            if -1 != line.find('Par.:'):
                entry['exemption'] = line.replace("Par.:", "")
                cur = cur + 1
            if -1 != line.find('Avsender:'):
                entry['sender'] = lines[cur+1].text
                cur = cur + 1
            if -1 != line.find('Mottaker:'):
                entry['recipient'] = lines[cur+1].text
                cur = cur + 1
            if -1 != line.find('Saksansv:'):
                entry['saksansvarlig'] = line.replace("Saksansv:", "").strip()
            if -1 != line.find('Saksbeh:'):
                entry['saksbehandler'] = lines[cur+1].text
                cur = cur + 1
                print entry
                scraperwiki.sqlite.save(unique_keys=['docid'], data=entry)
                entry = { 'agency' : agency, 'scrapedurl' : pdfurl }
            cur = cur + 1
        #return

def process_pdf(parser, pdfurl, errors):
    postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
    try:
    #if True:
        pdfcontent = scraperwiki.scrape(pdfurl)
        parse_pdf(pdfurl, pdfcontent)
        #parser.preprocess(pdfurl, pdfcontent)
        pdfcontent = None
#    except ValueError, e:
#        errors.append(e)
    #except IndexError, e:
    #    errors.append(e)
    except Exception, e:
        print e

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
    process_pdf(parser, "http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/getfile.php/rådhusets%20forvaltningstjeneste%20(RFT)/Intranett%20(RFT)/Dokumenter/Postjournal/11%20November/29112011.pdf", errors)
    process_pdf(parser, "http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/getfile.php/rådhusets%20forvaltningstjeneste%20(RFT)/Intranett%20(RFT)/Dokumenter/Postjournal/12%20Desember/02122011.pdf", errors)
    process_page_queue(parser, errors)
    report_errors(errors)
    exit(0)

errors = []
parser = postlistelib.PDFJournalParser(agency=agency)

#test_small_pdfs(parser)

process_journal_pdfs(parser, "http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/postjournal/", errors)
#process_page_queue(parser, errors)
report_errors(errors)

