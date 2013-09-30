# -*- coding: utf-8 -*-
#
# Python library for parsing public post journals (postlister) in Norway.
#

# Based on the scraper advanced-scraping-pdf
#
# See also
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/

# Possible sources using format 1 pdf:
# www.bydel-ullern.oslo.kommune.no
# www.gravferdsetaten.oslo.kommune.no
# www.halden.kommune.no (done)
# www.havn.oslo.kommune.no (done)
# www.hvaler.kommune.no (done)
# www.kafjord.kommune.no
# www.lier.kommune.no
# www.lindesnes.kommune.no
# www.naroy.kommune.no
# www.saltdal.kommune.no
# www.sogne.kommune.no
# www.vikna.kommune.no
#
# Google search to find more: "Offentlig journal" Seleksjon Sakstittel Dokumenttype Status filetype:pdf


import scraperwiki
import string
import re
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser

def cpu_spent():
    import resource
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

def exit_if_no_cpu_left(retval, callback=None, arg = None):
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    spent = cpu_spent()
    if soft < spent:
        if callback is not None:
            callback(arg, spent, hard, soft)
        print "Running out of CPU, exiting."
        exit(retval)

def fetch_url_harder(url, scraper = None):
    import urllib2
    html = None
    for n in [1, 2, 3]:
        try:
            if None == scraper:
                scraper = scraperwiki.scrape
            html = scraper(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

class JournalParser:
    agency = None
    debug = False

    validdoctypes = ['I', 'U', 'X', 'N']
    senderdoctypes = ['I', 'X', 'N']
    recipientdoctypes = ['U']
    mustfields = {
        'agency'         : 1,
        'docdesc'        : 1,
        'doctype'        : 1,
        'caseyear'       : 1,
        'caseseqnr'      : 1,
        'casedocseq'     : 1,
    }

    def __init__(self, agency):
        self.agency = agency

    def is_valid_doctype(self, doctype):
        return doctype in self.validdoctypes

    def is_sender_doctype(self, doctype):
        return doctype in self.senderdoctypes

    def is_recipient_doctype(self, doctype):
        return doctype in self.recipientdoctypes

    def verify_entry(self, entry):

        for field in self.mustfields:
            if not field in entry:
                raise ValueError("Missing required field " + field)

        if not self.is_valid_doctype(entry['doctype']):
            raise ValueError("Invalid doctype " + doctype)

        if -1 != entry['caseid'].find('-'):
            raise ValueError("Field caseid should not include dash: " + entry['caseid'])


        # Seen in http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200101_15012011.pdf
        if 'sender' in entry and -1 != entry['sender'].find("Side: "):
            raise ValueError("Field sender got page number, not real content")

#
# Parser of PDFs looking like
# http://www.storfjord.kommune.no/postliste-18-mai-2012.5056067-105358.html (type 1)
# http://www.hadsel.kommune.no/component/docman/doc_download/946-offentlig-postjournal-28032012 (type 2)
# http://www.stortinget.no/Global/pdf/postjournal/pj-2011-06-23.pdf (type 2 variant)
# Note sender/receiver is not yet parsed for type 2 PDFs
class PDFJournalParser(JournalParser):
    pagetable = "unparsedpages"
    brokenpagetable = "brokenpages"
    hiddentext = False
    breakonfailure = True

    def __init__(self, agency, hiddentext=False):
        self.hiddentext = hiddentext
        JournalParser.__init__(self, agency=agency)

    def is_already_scraped(self, url):
        # Ignore entries were sender and recipient is the result of a broken parser (before 2012-05-25)
        for sql in ["scrapedurl, sender, recipient from swdata where scrapedurl = '" + url + "' " +
        # FIXME Figure out why this do not work
        #" and not (sender = 'parse error' or recipient != 'parse error') " +
        "limit 1",

                    "scrapedurl from " + self.brokenpagetable + " where scrapedurl = '" + url + "' limit 1",
                    "scrapedurl from " + self.pagetable + " where scrapedurl = '" + url + "' limit 1"]:
            try:
                result = scraperwiki.sqlite.select(sql)
                #int sql, " : ", result
                if 0 < len(result) and u'scrapedurl' in result[0]:
                    return True
            except Exception as e:
                #if ('no such table: %s' % self.pagetable) not in str(e) and 'no such table: swdata' not in str(e):
                #    raise
                print "Exception: %s" % e
        return False

    # Check if we recognize the page content, and throw if not
    def is_valid_page(self, pdfurl, pagenum, pagecontent):
        s = BeautifulSoup(pagecontent)
        for t in s.findAll('text'):
            if t.text != " ":
#                if self.debug:
#                    print "'%s'" % t.text
                if 'Innhold:' == t.text: # type 1 or 2 (ePhorge)
                    s = None
                    return True
                if 'Arkivdel:' == t.text or 'Notater (X):' == t.text: # type 3 (doculive)
                    s = None
                    print "Found doculive (type 3)"
                    return True
        s = None
        if self.debug:
            print "Unrecognized page format for " + pdfurl
        raise ValueError("Unrecognized page format for " + pdfurl)

    #
    # Split PDF content into pages and store in SQL table for later processing.
    # The process is split in two to better handle parge PDFs (like 600 pages),
    # without running out of CPU time without loosing track of what is left to
    # parse.
    def preprocess(self, pdfurl, pdfcontent):
        print "Preprocessing PDF " + pdfurl
        if not pdfcontent:
            raise ValueError("No pdf content passed for " + pdfurl)
        if self.hiddentext:
            options = '-hidden'
        else:
            options = ''
        xml=scraperwiki.pdftoxml(pdfcontent, options)
#        if self.debug:
#            print xml
        pages=re.findall('(<page .+?</page>)',xml,flags=re.DOTALL)
        xml=None
#    print pages[:1][:1000]
        pagecount = 0
        datastore = []
        for page in pages:
            pagecount = pagecount + 1
            self.is_valid_page(pdfurl, pagecount, page)
            data = {
                'scrapedurl' : pdfurl,
                'pagenum' : pagecount,
                'pagecontent' : page,
            }
            datastore.append(data)
        if 0 < len(datastore):
            scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=datastore, table_name=self.pagetable)
        else:
            raise ValueError("Unable to find any pages in " + pdfurl)
        pages = None

    def fetch_and_preprocess(self, pdfurl):
        pdfcontent = fetch_url_harder(pdfurl)
        self.preprocess(pdfurl, pdfcontent)
        pdfcontent = None

    def print_entry(self, entrytext):
        for i in range(0, len(entrytext)):
            print str(i) + ": '" + entrytext[i] + "'"

    # ePhorte PDF
    def parse_entry_type1(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
             'agency' : self.agency,
             'scrapestamputc' : scrapestamputc,
             'scrapedurl' : pdfurl
             }
        i = 0
        while i < len(entrytext):
            #print "T: '" + entrytext[i] + "'"
            if 'Innhold:' == entrytext[i]:
                tittel = ""
                # handle multi-line titles
                while 'Sakstittel:' != entrytext[i+1]:
                    tittel = tittel + " " + entrytext[i+1]
                    i = i + 1
                entry['docdesc'] = tittel
            if 'Sakstittel:' == entrytext[i]:
                sakstittel = ""
                while 'DokType' != entrytext[i+1]:
#                    print "'" + entrytext[i+1] + "'"
                    sakstittel = sakstittel + " " + entrytext[i+1]
                    i = i + 1
                entry['casedesc'] = sakstittel
            if 'DokType' == entrytext[i]: # Values I/U/N/X from NOARK 4 table 14.2.11
                entry['doctype'] = entrytext[i+1]
                # As seen on http://www.saltdal.kommune.no/images/module.files/2007-05-16.pdf, page 1
                if entry['doctype'] == 'S':
                    entry['doctype'] = 'X'
                i = i + 1
            if 'Sak/dok nr:' == entrytext[i]:
            # FIXME Split and handle combined sak/løpenr
            # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
                caseid = None
                lnr = None
                if -1 != entrytext[i+4].find('penr.:'):
                    caseid = entrytext[i+1] + entrytext[i+2]
                    lnr = entrytext[i+3]
                    i = i + 4
                elif -1 != entrytext[i+3].find('penr.:'):
                    caseid = entrytext[i+1]
                    lnr = entrytext[i+2]
                    i = i + 3
                elif -1 != entrytext[i+2].find('penr.:'):
                    caseid, lnr = entrytext[i+1].split(" ")
                    i = i + 2

                caseyear, caseseqnr = caseid.split("/")
                entry['caseyear'] = int(caseyear)
                caseseqnr, casedocseq = caseseqnr.split("-")
                entry['caseseqnr'] = int(caseseqnr)
                entry['casedocseq'] = int(casedocseq)
                entry['caseid'] = caseyear + "/" + caseseqnr

                journalseqnr, journalyear = lnr.split("/")
                entry['journalid'] = journalyear + "/" + journalseqnr
                entry['journalyear'] = int(journalyear)
                entry['journalseqnr'] = int(journalseqnr)

#        if -1 != text[i].find('penr.:'): # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
#            str = text[i-1]
#            print "S: '" + str + "'"
#            data['journalid'] = str
#            # FIXME handle combined sak/løpenr
            if 'Journaldato:' == entrytext[i]:
                entry['recorddate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Dok.dato:' == entrytext[i]:
                entry['docdate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Tilg.kode Hjemmel:' == entrytext[i] and 'Avsender\mottaker:' != entrytext[i+1]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
            if 'Tilg.kode' == entrytext[i]:
                entry['accesscode'] = entrytext[i+1]
                i = i + 1
            if 'Hjemmel:' == entrytext[i]:
                 entry['exemption'] = entrytext[i+1]
                 i = i + 1
            if 'Avsender\mottaker:' == entrytext[i]:
                if i+1 < len(entrytext): # Non-empty field
                    fratil = entrytext[i+1]
                    i = i + 1
                    if self.is_sender_doctype(entry['doctype']):
                        entry['sender'] = fratil
                    elif self.is_recipient_doctype(entry['doctype']):
                        entry['recipient'] = fratil
                    else:
                        raise ValueError("Case " + entry['caseid'] + " Sender/Recipient with doctype " + entry['doctype'] + " != I/U/X/N in " + pdfurl)
            if self.debug:
                print entry
            i = i + 1
        return entry

    def parse_case_journal_ref(self, entry, reftext, pdfurl):
        try:
            # FIXME Split and handle combined sak/loepenr
            # Use find('penr.:') to avoid non-ascii search string 'Loepenr.:'
            caseid = None
            lnr = None
            if 4 == len(reftext):
#                print "4 " + str(reftext)
                caseid = reftext[0] + reftext[1]
                lnr = reftext[2] + reftext[3]
#                print str(caseid) + " " + str(lnr)
            elif 3 == len(reftext):
                if -1 != reftext[0].find("/") and -1 != reftext[2].find("/"):
#                    print "31"
                    caseid = reftext[0] + reftext[1]
                    lnr = reftext[2]
                elif -1 != reftext[2].find("/"):
#                    print "32"
                    caseid = reftext[0] + reftext[1]
                    lnr = reftext[2]
                elif -1 == reftext[2].find("/"):
#                    print "33"
                    caseid = reftext[0]
                    lnr = reftext[1] + reftext[2]
            elif 2 == len(reftext):
                if -1 == reftext[1].find("/"):
#                    print "21"
                    s = reftext[0] + reftext[1]
#                    print "S: " + s
                    caseid, lnr = s.split(" ")
                elif -1 != reftext[1].find("/"):
#                    print "22"
                    caseid = reftext[0]
                    lnr = reftext[1]
            elif 1 == len(reftext):
                caseid, lnr  = reftext[0].split(" ")
            else:
                raise ValueError("Unable to parse entry " + str(reftext) + " in " + pdfurl)
#            print "C: " + caseid + " L: " + lnr

            caseyear, caseseqnr = caseid.split("/")
            entry['caseyear'] = int(caseyear)
            caseseqnr, casedocseq = caseseqnr.split("-")
            entry['caseseqnr'] = int(caseseqnr)
            entry['casedocseq'] = int(casedocseq)
            entry['caseid'] = caseyear + "/" + caseseqnr

            journalseqnr, journalyear = lnr.split("/")
            entry['journalid'] = journalyear + "/" + journalseqnr
            entry['journalyear'] = int(journalyear)
            entry['journalseqnr'] = int(journalseqnr)
        except:
            print "Unable to parse " + str(reftext)
        return entry
    def test_parse_case_journal_ref(self):
        entry = {}
        self.parse_case_journal_ref(entry, [u'2008/16414-', u'23', u'15060/2012'], "")
        self.parse_case_journal_ref(entry, [u'2011/15972-1 102773/201', u'1'], "")
        self.parse_case_journal_ref(entry, [u'2010/2593-2', u'103004/201', u'1'], "")
        self.parse_case_journal_ref(entry, [u'2011/13415-', u'22', u'100077/201', u'1'], "")

    # ePhorte PDF
    def parse_entry_type2(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
            'agency' : self.agency,
            'scrapestamputc' : scrapestamputc,
            'scrapedurl' : pdfurl
            }
        i = 0
        avsender = []
        mottaker = []
        while i < len(entrytext):
            if 'Innhold:' == entrytext[i]:
                tittel = ""
                # handle multi-line titles
                while 'Sakstittel:' != entrytext[i+1]:
                    tittel = tittel + entrytext[i+1]
                    i = i + 1
                entry['docdesc'] = tittel
            if 'Sakstittel:' == entrytext[i]:
                sakstittel = ""
                # Klassering er i en annen dokumenttype
                while 'DokType' != entrytext[i+1] and 'Dok.Type:' != entrytext[i+1] and 'Klassering:' != entrytext[i+1]:

#                print "'" + entrytext[i+1] + "'"
                    sakstittel = sakstittel + entrytext[i+1]
                    i = i + 1
                entry['casedesc'] = sakstittel
                i = i + 1
            if 'DokType' == entrytext[i] or 'Dok.Type:' == entrytext[i]: # Values I/U/N/X from NOARK 4 table 14.2.11
                entry['doctype'] = entrytext[i+1]
                # As seen on http://www.uis.no/getfile.php/Journal%20200612.pdf
                if entry['doctype'] == 'S':
                    entry['doctype'] = 'X'
                i = i + 1
            if 'Sak/dok nr:' == entrytext[i] or 'Sak/dok.nr:' == entrytext[i]:
                endi = i
                while endi < len(entrytext):
                    if -1 != entrytext[endi].find('penr.:') or -1 != entrytext[endi].find('penr:'):
                        break
                    endi = endi + 1
                entry = self.parse_case_journal_ref(entry, entrytext[i+1:endi], pdfurl)
                i = endi + 1
#       if -1 != text[i].find('penr.:'): # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
#                str = text[i-1]
#                print "S: '" + str + "'"
#                data['journalid'] = str
#                # FIXME handle combined sak/løpenr
            if 'Journaldato:' == entrytext[i]:
                entry['recorddate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Dok.dato:' == entrytext[i]:
                entry['docdate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Tilg.kode Hjemmel:' == entrytext[i] and '(enhet/initialer):' != entrytext[i+2]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
            if 'Tilg.kode' == entrytext[i]:
                entry['accesscode'] = entrytext[i+1]
                i = i + 1
            if 'Hjemmel:' == entrytext[i]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
#        if -1 != text[i].find('Avs./mottaker:'):
# FIXME Need to handle senders and receivers
            if 'Mottaker' == entrytext[i]:
                mottaker.append(entrytext[i-1])
            if 'Avsender' == entrytext[i]:
                avsender.append(entrytext[i-1])
#            entry['sender'] = 'parse error'
#            entry['recipient'] = 'parse error'
            i = i + 1
        if 0 < len(mottaker):
            entry['recipient'] = string.join(mottaker, ", ")
        if 0 < len(avsender):
            entry['sender'] = string.join(avsender, ", ")
        return entry

    def parse_entry_type3(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
            'agency' : self.agency,
            'scrapestamputc' : scrapestamputc,
            'scrapedurl' : pdfurl
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
        return entry

    def parse_page(self, pdfurl, pagenum, pagecontent):
        print "Scraping " + pdfurl + " page " + str(pagenum)
        s = BeautifulSoup(pagecontent)
        datastore = []
        text = []
        linecount = 0
        if self.debug:
            print s
        for t in s.findAll('text'):
            if t.text != " ":
                text.append(t.text)
                if self.debug:
                    print str(linecount) + ": " + t.text
# FIXME Remove length limit when working
#        if 100 <= linecount:
#            break
            linecount = linecount + 1
#        if -1 != t.text.find("Side:"):
#            print t.text
        s = None

#    print "Found " + str(linecount) + " lines/text fragments in the PDF"
        if len(text) < linecount:
            raise  ValueError("Text array too sort!")

        # First count how many entries to expect on this page, to be able to
        # verify that all of them were found.
        entrycount = 0
        i = 0
        while i < len(text):
            # Type 1 and 2 (ePhorge)
            if 'Innhold:' == text[i] or \
               'Arkivdel:' == text[i]:  # type 3 (doculive)
                entrycount = entrycount + 1
            i = i + 1

        i = 0
        while i < len(text):
            if self.debug:
                print "T: '" + text[i] + "'"
            if self.debug and -1 != text[i].find("Side:"):
                print text[i]
            if 'Innhold:' == text[i]:
                endi = i + 1
                pdfparser = None
                format = "unknown"
                while endi < len(text):
                    if 'Klassering:' == text[endi]:
                        print "Found ePhorte PDF (type 1)"
                        pdfparser = self.parse_entry_type2
                        format = "type2"
                    if 'Avsender\mottaker:' == text[endi]:
                        print "Found ePhorge PDF (type 2)"
                        pdfparser = self.parse_entry_type1
                        format = "type1"
                    if 'Arkivdel:' == text[endi]:
                        print "Found Doculive PDF"
                        pdfparser = self.parse_entry_type3
                        format = "type3"
                    if 'Innhold:' == text[endi]:
                        break
                    endi = endi + 1
                if self.debug:
                    print "Entry " + str(entrycount) + " from " + str(i) + " to " + str(endi) + " ie " + str(endi - i) + " lines"
                try:
                    if pdfparser is None:
                        raise ValueError("Unrecognized page format in " + pdfurl)
                    entry = pdfparser(text[i:endi], pdfurl)
                    if 'caseid' not in entry or entry['caseid'] is None or \
                       not self.is_valid_doctype(entry['doctype']):
                        raise ValueError("Unable to parse " + pdfurl + " as format " + format + " [" + str(entry) + "]")
#                print entry
                    datastore.append(entry)
                    i = endi - 2
                except:
                    self.print_entry(text[i:endi])
                    raise
            i = i + 1
#        print data
#    print "Found " + str(len(datastore)) + " of " + str(entrycount) + " entries"
        if entrycount != len(datastore):
#        print text
            raise ValueError("Unable to parse all entries in " + pdfurl)
        if 0 == len(datastore):
            print "Unable to find any entries in " + pdfurl
        else:
            scraperwiki.sqlite.save(unique_keys=['caseid', 'casedocseq'], data=datastore)
        datastore = None
        text = None

    def process_pages(self):
        brokenpages = 0
        try:
            sqlselect = "* from " + self.pagetable + " limit 1"
            pageref = scraperwiki.sqlite.select(sqlselect)
            while pageref:
                scrapedurl = pageref[0]['scrapedurl']
                pagenum = pageref[0]['pagenum']
                pagecontent = pageref[0]['pagecontent']
#            print "Found " + scrapedurl + " page " + str(pagenum) + " length " + str(len(pagecontent))
                try:
                    sqldelete = "delete from " + self.pagetable + " where scrapedurl = '" + scrapedurl + "' and pagenum = " + str(pagenum)
                    self.parse_page(scrapedurl, pagenum, pagecontent)
#                    print "Trying to: " + sqldelete
                    scraperwiki.sqlite.execute(sqldelete)
                except ValueError, e:
                    brokenpage = {
                        'scrapedurl' : scrapedurl,
                        'pagenum' : pagenum,
                        'pagecontent' : pagecontent,
                        'failstamp' : datetime.datetime.now(),
                    }
                    print "Unsupported page %d from %s" % (pagenum, scrapedurl)
                    brokenpages = brokenpages + 1
                    scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=brokenpage, table_name=self.brokenpagetable)
                scraperwiki.sqlite.execute(sqldelete)
                scraperwiki.sqlite.commit()
                pageref = scraperwiki.sqlite.select(sqlselect)

            # Last, try some of the broken pages again, in case we got support for handling them in the mean time
            try:
                # First, check if the table exist
                scraperwiki.sqlite.execute("select * from " + self.brokenpagetable)

                newtrystamp = datetime.datetime.now()
                sqlselect = "* from " + self.brokenpagetable + " where failstamp is NULL or failstamp < '" + str(newtrystamp) + "'" + " limit 1"
                try:
                    pageref = scraperwiki.sqlite.select(sqlselect)
                except scraperwiki.sqlite.SqliteError, e:
                    scraperwiki.sqlite.execute("ALTER TABLE " + self.brokenpagetable + " ADD COLUMN failstamp")
                    scraperwiki.sqlite.commit()
                    pageref = scraperwiki.sqlite.select(sqlselect)

                pagelimit = 10
                while pageref and 0 < pagelimit:
                    pagelimit = pagelimit - 1
                    scrapedurl = pageref[0]['scrapedurl']
                    pagenum = pageref[0]['pagenum']
                    pagecontent = pageref[0]['pagecontent']
#                    print "Found " + scrapedurl + " page " + str(pagenum) + " length " + str(len(pagecontent))
                    try:
                        sqldelete = "delete from " + self.brokenpagetable + " where scrapedurl = '" + scrapedurl + "' and pagenum = " + str(pagenum)
                        self.parse_page(scrapedurl, pagenum, pagecontent)
#                    print "Trying to: " + sqldelete
                        scraperwiki.sqlite.execute(sqldelete)
                    except ValueError, e:
                        brokenpage = {
                            'scrapedurl' : scrapedurl,
                            'pagenum' : pagenum,
                            'pagecontent' : pagecontent,
                            'failstamp' : newtrystamp,
                        }
                    
                        print "Still unsupported page %d from %s" % (pagenum, scrapedurl)
                        brokenpages = brokenpages + 1
                        scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=brokenpage, table_name=self.brokenpagetable)
                    scraperwiki.sqlite.commit()
                    pageref = scraperwiki.sqlite.select(sqlselect)
            except:
                True # Ignore missing brokenpages table
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)
            raise
        if 0 < brokenpages:
            raise ValueError("Found %d pages with unsupported format" % brokenpages)

def fieldlist():
    import urllib2
    import json

    scrapers = [
        'postliste-universitetet-i-oslo',
        'postliste-lindesnes',
        'postliste-kristiansund',
        'postliste-stortinget',
        'postliste-arendal',
        'postliste-oep',
        'postliste-ballangen',
        'postliste-hadsel',
        'postliste-storfjord',
        'postliste-oslo-havn',
      ]

    keys = {}

    for scraper in scrapers:
        url = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=' + scraper + '&version=-1'
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        if 'swdata' in data[0]['datasummary']['tables']:
            for key in data[0]['datasummary']['tables']['swdata']['keys']:
                key = key.lower()
                if key in keys:
                    keys[key].append(scraper)
                else:
                    keys[key] = [scraper]
    def lensort(a, b):
        return cmp(len(keys[b]), len(keys[a]))

    for key in sorted(keys.keys(), lensort):
        print len(keys[key]), key, str(keys[key])

def test_parser():
    parser = PDFJournalParser(agency="Dummy agency")
    parser.debug = True
    for url in [ #"http://www.stortinget.no/Global/pdf/postjournal/pj-2011-06-23.pdf",
                "http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/getfile.php/rådhusets%20forvaltningstjeneste%20(RFT)/Intranett%20(RFT)/Dokumenter/Postjournal/11%20November/29112011.pdf",
        ]:
        pdfcontent = scraperwiki.scrape(url)
        parser.preprocess(url,pdfcontent)
        parser.process_pages()

if __name__ == "scraper" or __name__ == '__main__':
    test_parser()
#    fieldlist()

# -*- coding: utf-8 -*-
#
# Python library for parsing public post journals (postlister) in Norway.
#

# Based on the scraper advanced-scraping-pdf
#
# See also
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/

# Possible sources using format 1 pdf:
# www.bydel-ullern.oslo.kommune.no
# www.gravferdsetaten.oslo.kommune.no
# www.halden.kommune.no (done)
# www.havn.oslo.kommune.no (done)
# www.hvaler.kommune.no (done)
# www.kafjord.kommune.no
# www.lier.kommune.no
# www.lindesnes.kommune.no
# www.naroy.kommune.no
# www.saltdal.kommune.no
# www.sogne.kommune.no
# www.vikna.kommune.no
#
# Google search to find more: "Offentlig journal" Seleksjon Sakstittel Dokumenttype Status filetype:pdf


import scraperwiki
import string
import re
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser

def cpu_spent():
    import resource
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

def exit_if_no_cpu_left(retval, callback=None, arg = None):
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    spent = cpu_spent()
    if soft < spent:
        if callback is not None:
            callback(arg, spent, hard, soft)
        print "Running out of CPU, exiting."
        exit(retval)

def fetch_url_harder(url, scraper = None):
    import urllib2
    html = None
    for n in [1, 2, 3]:
        try:
            if None == scraper:
                scraper = scraperwiki.scrape
            html = scraper(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

class JournalParser:
    agency = None
    debug = False

    validdoctypes = ['I', 'U', 'X', 'N']
    senderdoctypes = ['I', 'X', 'N']
    recipientdoctypes = ['U']
    mustfields = {
        'agency'         : 1,
        'docdesc'        : 1,
        'doctype'        : 1,
        'caseyear'       : 1,
        'caseseqnr'      : 1,
        'casedocseq'     : 1,
    }

    def __init__(self, agency):
        self.agency = agency

    def is_valid_doctype(self, doctype):
        return doctype in self.validdoctypes

    def is_sender_doctype(self, doctype):
        return doctype in self.senderdoctypes

    def is_recipient_doctype(self, doctype):
        return doctype in self.recipientdoctypes

    def verify_entry(self, entry):

        for field in self.mustfields:
            if not field in entry:
                raise ValueError("Missing required field " + field)

        if not self.is_valid_doctype(entry['doctype']):
            raise ValueError("Invalid doctype " + doctype)

        if -1 != entry['caseid'].find('-'):
            raise ValueError("Field caseid should not include dash: " + entry['caseid'])


        # Seen in http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200101_15012011.pdf
        if 'sender' in entry and -1 != entry['sender'].find("Side: "):
            raise ValueError("Field sender got page number, not real content")

#
# Parser of PDFs looking like
# http://www.storfjord.kommune.no/postliste-18-mai-2012.5056067-105358.html (type 1)
# http://www.hadsel.kommune.no/component/docman/doc_download/946-offentlig-postjournal-28032012 (type 2)
# http://www.stortinget.no/Global/pdf/postjournal/pj-2011-06-23.pdf (type 2 variant)
# Note sender/receiver is not yet parsed for type 2 PDFs
class PDFJournalParser(JournalParser):
    pagetable = "unparsedpages"
    brokenpagetable = "brokenpages"
    hiddentext = False
    breakonfailure = True

    def __init__(self, agency, hiddentext=False):
        self.hiddentext = hiddentext
        JournalParser.__init__(self, agency=agency)

    def is_already_scraped(self, url):
        # Ignore entries were sender and recipient is the result of a broken parser (before 2012-05-25)
        for sql in ["scrapedurl, sender, recipient from swdata where scrapedurl = '" + url + "' " +
        # FIXME Figure out why this do not work
        #" and not (sender = 'parse error' or recipient != 'parse error') " +
        "limit 1",

                    "scrapedurl from " + self.brokenpagetable + " where scrapedurl = '" + url + "' limit 1",
                    "scrapedurl from " + self.pagetable + " where scrapedurl = '" + url + "' limit 1"]:
            try:
                result = scraperwiki.sqlite.select(sql)
                #int sql, " : ", result
                if 0 < len(result) and u'scrapedurl' in result[0]:
                    return True
            except Exception as e:
                #if ('no such table: %s' % self.pagetable) not in str(e) and 'no such table: swdata' not in str(e):
                #    raise
                print "Exception: %s" % e
        return False

    # Check if we recognize the page content, and throw if not
    def is_valid_page(self, pdfurl, pagenum, pagecontent):
        s = BeautifulSoup(pagecontent)
        for t in s.findAll('text'):
            if t.text != " ":
#                if self.debug:
#                    print "'%s'" % t.text
                if 'Innhold:' == t.text: # type 1 or 2 (ePhorge)
                    s = None
                    return True
                if 'Arkivdel:' == t.text or 'Notater (X):' == t.text: # type 3 (doculive)
                    s = None
                    print "Found doculive (type 3)"
                    return True
        s = None
        if self.debug:
            print "Unrecognized page format for " + pdfurl
        raise ValueError("Unrecognized page format for " + pdfurl)

    #
    # Split PDF content into pages and store in SQL table for later processing.
    # The process is split in two to better handle parge PDFs (like 600 pages),
    # without running out of CPU time without loosing track of what is left to
    # parse.
    def preprocess(self, pdfurl, pdfcontent):
        print "Preprocessing PDF " + pdfurl
        if not pdfcontent:
            raise ValueError("No pdf content passed for " + pdfurl)
        if self.hiddentext:
            options = '-hidden'
        else:
            options = ''
        xml=scraperwiki.pdftoxml(pdfcontent, options)
#        if self.debug:
#            print xml
        pages=re.findall('(<page .+?</page>)',xml,flags=re.DOTALL)
        xml=None
#    print pages[:1][:1000]
        pagecount = 0
        datastore = []
        for page in pages:
            pagecount = pagecount + 1
            self.is_valid_page(pdfurl, pagecount, page)
            data = {
                'scrapedurl' : pdfurl,
                'pagenum' : pagecount,
                'pagecontent' : page,
            }
            datastore.append(data)
        if 0 < len(datastore):
            scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=datastore, table_name=self.pagetable)
        else:
            raise ValueError("Unable to find any pages in " + pdfurl)
        pages = None

    def fetch_and_preprocess(self, pdfurl):
        pdfcontent = fetch_url_harder(pdfurl)
        self.preprocess(pdfurl, pdfcontent)
        pdfcontent = None

    def print_entry(self, entrytext):
        for i in range(0, len(entrytext)):
            print str(i) + ": '" + entrytext[i] + "'"

    # ePhorte PDF
    def parse_entry_type1(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
             'agency' : self.agency,
             'scrapestamputc' : scrapestamputc,
             'scrapedurl' : pdfurl
             }
        i = 0
        while i < len(entrytext):
            #print "T: '" + entrytext[i] + "'"
            if 'Innhold:' == entrytext[i]:
                tittel = ""
                # handle multi-line titles
                while 'Sakstittel:' != entrytext[i+1]:
                    tittel = tittel + " " + entrytext[i+1]
                    i = i + 1
                entry['docdesc'] = tittel
            if 'Sakstittel:' == entrytext[i]:
                sakstittel = ""
                while 'DokType' != entrytext[i+1]:
#                    print "'" + entrytext[i+1] + "'"
                    sakstittel = sakstittel + " " + entrytext[i+1]
                    i = i + 1
                entry['casedesc'] = sakstittel
            if 'DokType' == entrytext[i]: # Values I/U/N/X from NOARK 4 table 14.2.11
                entry['doctype'] = entrytext[i+1]
                # As seen on http://www.saltdal.kommune.no/images/module.files/2007-05-16.pdf, page 1
                if entry['doctype'] == 'S':
                    entry['doctype'] = 'X'
                i = i + 1
            if 'Sak/dok nr:' == entrytext[i]:
            # FIXME Split and handle combined sak/løpenr
            # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
                caseid = None
                lnr = None
                if -1 != entrytext[i+4].find('penr.:'):
                    caseid = entrytext[i+1] + entrytext[i+2]
                    lnr = entrytext[i+3]
                    i = i + 4
                elif -1 != entrytext[i+3].find('penr.:'):
                    caseid = entrytext[i+1]
                    lnr = entrytext[i+2]
                    i = i + 3
                elif -1 != entrytext[i+2].find('penr.:'):
                    caseid, lnr = entrytext[i+1].split(" ")
                    i = i + 2

                caseyear, caseseqnr = caseid.split("/")
                entry['caseyear'] = int(caseyear)
                caseseqnr, casedocseq = caseseqnr.split("-")
                entry['caseseqnr'] = int(caseseqnr)
                entry['casedocseq'] = int(casedocseq)
                entry['caseid'] = caseyear + "/" + caseseqnr

                journalseqnr, journalyear = lnr.split("/")
                entry['journalid'] = journalyear + "/" + journalseqnr
                entry['journalyear'] = int(journalyear)
                entry['journalseqnr'] = int(journalseqnr)

#        if -1 != text[i].find('penr.:'): # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
#            str = text[i-1]
#            print "S: '" + str + "'"
#            data['journalid'] = str
#            # FIXME handle combined sak/løpenr
            if 'Journaldato:' == entrytext[i]:
                entry['recorddate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Dok.dato:' == entrytext[i]:
                entry['docdate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Tilg.kode Hjemmel:' == entrytext[i] and 'Avsender\mottaker:' != entrytext[i+1]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
            if 'Tilg.kode' == entrytext[i]:
                entry['accesscode'] = entrytext[i+1]
                i = i + 1
            if 'Hjemmel:' == entrytext[i]:
                 entry['exemption'] = entrytext[i+1]
                 i = i + 1
            if 'Avsender\mottaker:' == entrytext[i]:
                if i+1 < len(entrytext): # Non-empty field
                    fratil = entrytext[i+1]
                    i = i + 1
                    if self.is_sender_doctype(entry['doctype']):
                        entry['sender'] = fratil
                    elif self.is_recipient_doctype(entry['doctype']):
                        entry['recipient'] = fratil
                    else:
                        raise ValueError("Case " + entry['caseid'] + " Sender/Recipient with doctype " + entry['doctype'] + " != I/U/X/N in " + pdfurl)
            if self.debug:
                print entry
            i = i + 1
        return entry

    def parse_case_journal_ref(self, entry, reftext, pdfurl):
        try:
            # FIXME Split and handle combined sak/loepenr
            # Use find('penr.:') to avoid non-ascii search string 'Loepenr.:'
            caseid = None
            lnr = None
            if 4 == len(reftext):
#                print "4 " + str(reftext)
                caseid = reftext[0] + reftext[1]
                lnr = reftext[2] + reftext[3]
#                print str(caseid) + " " + str(lnr)
            elif 3 == len(reftext):
                if -1 != reftext[0].find("/") and -1 != reftext[2].find("/"):
#                    print "31"
                    caseid = reftext[0] + reftext[1]
                    lnr = reftext[2]
                elif -1 != reftext[2].find("/"):
#                    print "32"
                    caseid = reftext[0] + reftext[1]
                    lnr = reftext[2]
                elif -1 == reftext[2].find("/"):
#                    print "33"
                    caseid = reftext[0]
                    lnr = reftext[1] + reftext[2]
            elif 2 == len(reftext):
                if -1 == reftext[1].find("/"):
#                    print "21"
                    s = reftext[0] + reftext[1]
#                    print "S: " + s
                    caseid, lnr = s.split(" ")
                elif -1 != reftext[1].find("/"):
#                    print "22"
                    caseid = reftext[0]
                    lnr = reftext[1]
            elif 1 == len(reftext):
                caseid, lnr  = reftext[0].split(" ")
            else:
                raise ValueError("Unable to parse entry " + str(reftext) + " in " + pdfurl)
#            print "C: " + caseid + " L: " + lnr

            caseyear, caseseqnr = caseid.split("/")
            entry['caseyear'] = int(caseyear)
            caseseqnr, casedocseq = caseseqnr.split("-")
            entry['caseseqnr'] = int(caseseqnr)
            entry['casedocseq'] = int(casedocseq)
            entry['caseid'] = caseyear + "/" + caseseqnr

            journalseqnr, journalyear = lnr.split("/")
            entry['journalid'] = journalyear + "/" + journalseqnr
            entry['journalyear'] = int(journalyear)
            entry['journalseqnr'] = int(journalseqnr)
        except:
            print "Unable to parse " + str(reftext)
        return entry
    def test_parse_case_journal_ref(self):
        entry = {}
        self.parse_case_journal_ref(entry, [u'2008/16414-', u'23', u'15060/2012'], "")
        self.parse_case_journal_ref(entry, [u'2011/15972-1 102773/201', u'1'], "")
        self.parse_case_journal_ref(entry, [u'2010/2593-2', u'103004/201', u'1'], "")
        self.parse_case_journal_ref(entry, [u'2011/13415-', u'22', u'100077/201', u'1'], "")

    # ePhorte PDF
    def parse_entry_type2(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
            'agency' : self.agency,
            'scrapestamputc' : scrapestamputc,
            'scrapedurl' : pdfurl
            }
        i = 0
        avsender = []
        mottaker = []
        while i < len(entrytext):
            if 'Innhold:' == entrytext[i]:
                tittel = ""
                # handle multi-line titles
                while 'Sakstittel:' != entrytext[i+1]:
                    tittel = tittel + entrytext[i+1]
                    i = i + 1
                entry['docdesc'] = tittel
            if 'Sakstittel:' == entrytext[i]:
                sakstittel = ""
                # Klassering er i en annen dokumenttype
                while 'DokType' != entrytext[i+1] and 'Dok.Type:' != entrytext[i+1] and 'Klassering:' != entrytext[i+1]:

#                print "'" + entrytext[i+1] + "'"
                    sakstittel = sakstittel + entrytext[i+1]
                    i = i + 1
                entry['casedesc'] = sakstittel
                i = i + 1
            if 'DokType' == entrytext[i] or 'Dok.Type:' == entrytext[i]: # Values I/U/N/X from NOARK 4 table 14.2.11
                entry['doctype'] = entrytext[i+1]
                # As seen on http://www.uis.no/getfile.php/Journal%20200612.pdf
                if entry['doctype'] == 'S':
                    entry['doctype'] = 'X'
                i = i + 1
            if 'Sak/dok nr:' == entrytext[i] or 'Sak/dok.nr:' == entrytext[i]:
                endi = i
                while endi < len(entrytext):
                    if -1 != entrytext[endi].find('penr.:') or -1 != entrytext[endi].find('penr:'):
                        break
                    endi = endi + 1
                entry = self.parse_case_journal_ref(entry, entrytext[i+1:endi], pdfurl)
                i = endi + 1
#       if -1 != text[i].find('penr.:'): # Use find('penr.:') to avoid non-ascii search string 'Løpenr.:'
#                str = text[i-1]
#                print "S: '" + str + "'"
#                data['journalid'] = str
#                # FIXME handle combined sak/løpenr
            if 'Journaldato:' == entrytext[i]:
                entry['recorddate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Dok.dato:' == entrytext[i]:
                entry['docdate'] = dateutil.parser.parse(entrytext[i-1], dayfirst=True)
            if 'Tilg.kode Hjemmel:' == entrytext[i] and '(enhet/initialer):' != entrytext[i+2]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
            if 'Tilg.kode' == entrytext[i]:
                entry['accesscode'] = entrytext[i+1]
                i = i + 1
            if 'Hjemmel:' == entrytext[i]:
                entry['exemption'] = entrytext[i+1]
                i = i + 1
#        if -1 != text[i].find('Avs./mottaker:'):
# FIXME Need to handle senders and receivers
            if 'Mottaker' == entrytext[i]:
                mottaker.append(entrytext[i-1])
            if 'Avsender' == entrytext[i]:
                avsender.append(entrytext[i-1])
#            entry['sender'] = 'parse error'
#            entry['recipient'] = 'parse error'
            i = i + 1
        if 0 < len(mottaker):
            entry['recipient'] = string.join(mottaker, ", ")
        if 0 < len(avsender):
            entry['sender'] = string.join(avsender, ", ")
        return entry

    def parse_entry_type3(self, entrytext, pdfurl):
        scrapestamputc = datetime.datetime.now()
        entry = {
            'agency' : self.agency,
            'scrapestamputc' : scrapestamputc,
            'scrapedurl' : pdfurl
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
        return entry

    def parse_page(self, pdfurl, pagenum, pagecontent):
        print "Scraping " + pdfurl + " page " + str(pagenum)
        s = BeautifulSoup(pagecontent)
        datastore = []
        text = []
        linecount = 0
        if self.debug:
            print s
        for t in s.findAll('text'):
            if t.text != " ":
                text.append(t.text)
                if self.debug:
                    print str(linecount) + ": " + t.text
# FIXME Remove length limit when working
#        if 100 <= linecount:
#            break
            linecount = linecount + 1
#        if -1 != t.text.find("Side:"):
#            print t.text
        s = None

#    print "Found " + str(linecount) + " lines/text fragments in the PDF"
        if len(text) < linecount:
            raise  ValueError("Text array too sort!")

        # First count how many entries to expect on this page, to be able to
        # verify that all of them were found.
        entrycount = 0
        i = 0
        while i < len(text):
            # Type 1 and 2 (ePhorge)
            if 'Innhold:' == text[i] or \
               'Arkivdel:' == text[i]:  # type 3 (doculive)
                entrycount = entrycount + 1
            i = i + 1

        i = 0
        while i < len(text):
            if self.debug:
                print "T: '" + text[i] + "'"
            if self.debug and -1 != text[i].find("Side:"):
                print text[i]
            if 'Innhold:' == text[i]:
                endi = i + 1
                pdfparser = None
                format = "unknown"
                while endi < len(text):
                    if 'Klassering:' == text[endi]:
                        print "Found ePhorte PDF (type 1)"
                        pdfparser = self.parse_entry_type2
                        format = "type2"
                    if 'Avsender\mottaker:' == text[endi]:
                        print "Found ePhorge PDF (type 2)"
                        pdfparser = self.parse_entry_type1
                        format = "type1"
                    if 'Arkivdel:' == text[endi]:
                        print "Found Doculive PDF"
                        pdfparser = self.parse_entry_type3
                        format = "type3"
                    if 'Innhold:' == text[endi]:
                        break
                    endi = endi + 1
                if self.debug:
                    print "Entry " + str(entrycount) + " from " + str(i) + " to " + str(endi) + " ie " + str(endi - i) + " lines"
                try:
                    if pdfparser is None:
                        raise ValueError("Unrecognized page format in " + pdfurl)
                    entry = pdfparser(text[i:endi], pdfurl)
                    if 'caseid' not in entry or entry['caseid'] is None or \
                       not self.is_valid_doctype(entry['doctype']):
                        raise ValueError("Unable to parse " + pdfurl + " as format " + format + " [" + str(entry) + "]")
#                print entry
                    datastore.append(entry)
                    i = endi - 2
                except:
                    self.print_entry(text[i:endi])
                    raise
            i = i + 1
#        print data
#    print "Found " + str(len(datastore)) + " of " + str(entrycount) + " entries"
        if entrycount != len(datastore):
#        print text
            raise ValueError("Unable to parse all entries in " + pdfurl)
        if 0 == len(datastore):
            print "Unable to find any entries in " + pdfurl
        else:
            scraperwiki.sqlite.save(unique_keys=['caseid', 'casedocseq'], data=datastore)
        datastore = None
        text = None

    def process_pages(self):
        brokenpages = 0
        try:
            sqlselect = "* from " + self.pagetable + " limit 1"
            pageref = scraperwiki.sqlite.select(sqlselect)
            while pageref:
                scrapedurl = pageref[0]['scrapedurl']
                pagenum = pageref[0]['pagenum']
                pagecontent = pageref[0]['pagecontent']
#            print "Found " + scrapedurl + " page " + str(pagenum) + " length " + str(len(pagecontent))
                try:
                    sqldelete = "delete from " + self.pagetable + " where scrapedurl = '" + scrapedurl + "' and pagenum = " + str(pagenum)
                    self.parse_page(scrapedurl, pagenum, pagecontent)
#                    print "Trying to: " + sqldelete
                    scraperwiki.sqlite.execute(sqldelete)
                except ValueError, e:
                    brokenpage = {
                        'scrapedurl' : scrapedurl,
                        'pagenum' : pagenum,
                        'pagecontent' : pagecontent,
                        'failstamp' : datetime.datetime.now(),
                    }
                    print "Unsupported page %d from %s" % (pagenum, scrapedurl)
                    brokenpages = brokenpages + 1
                    scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=brokenpage, table_name=self.brokenpagetable)
                scraperwiki.sqlite.execute(sqldelete)
                scraperwiki.sqlite.commit()
                pageref = scraperwiki.sqlite.select(sqlselect)

            # Last, try some of the broken pages again, in case we got support for handling them in the mean time
            try:
                # First, check if the table exist
                scraperwiki.sqlite.execute("select * from " + self.brokenpagetable)

                newtrystamp = datetime.datetime.now()
                sqlselect = "* from " + self.brokenpagetable + " where failstamp is NULL or failstamp < '" + str(newtrystamp) + "'" + " limit 1"
                try:
                    pageref = scraperwiki.sqlite.select(sqlselect)
                except scraperwiki.sqlite.SqliteError, e:
                    scraperwiki.sqlite.execute("ALTER TABLE " + self.brokenpagetable + " ADD COLUMN failstamp")
                    scraperwiki.sqlite.commit()
                    pageref = scraperwiki.sqlite.select(sqlselect)

                pagelimit = 10
                while pageref and 0 < pagelimit:
                    pagelimit = pagelimit - 1
                    scrapedurl = pageref[0]['scrapedurl']
                    pagenum = pageref[0]['pagenum']
                    pagecontent = pageref[0]['pagecontent']
#                    print "Found " + scrapedurl + " page " + str(pagenum) + " length " + str(len(pagecontent))
                    try:
                        sqldelete = "delete from " + self.brokenpagetable + " where scrapedurl = '" + scrapedurl + "' and pagenum = " + str(pagenum)
                        self.parse_page(scrapedurl, pagenum, pagecontent)
#                    print "Trying to: " + sqldelete
                        scraperwiki.sqlite.execute(sqldelete)
                    except ValueError, e:
                        brokenpage = {
                            'scrapedurl' : scrapedurl,
                            'pagenum' : pagenum,
                            'pagecontent' : pagecontent,
                            'failstamp' : newtrystamp,
                        }
                    
                        print "Still unsupported page %d from %s" % (pagenum, scrapedurl)
                        brokenpages = brokenpages + 1
                        scraperwiki.sqlite.save(unique_keys=['scrapedurl', 'pagenum'], data=brokenpage, table_name=self.brokenpagetable)
                    scraperwiki.sqlite.commit()
                    pageref = scraperwiki.sqlite.select(sqlselect)
            except:
                True # Ignore missing brokenpages table
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)
            raise
        if 0 < brokenpages:
            raise ValueError("Found %d pages with unsupported format" % brokenpages)

def fieldlist():
    import urllib2
    import json

    scrapers = [
        'postliste-universitetet-i-oslo',
        'postliste-lindesnes',
        'postliste-kristiansund',
        'postliste-stortinget',
        'postliste-arendal',
        'postliste-oep',
        'postliste-ballangen',
        'postliste-hadsel',
        'postliste-storfjord',
        'postliste-oslo-havn',
      ]

    keys = {}

    for scraper in scrapers:
        url = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=' + scraper + '&version=-1'
        response = urllib2.urlopen(url)
        html = response.read()
        data = json.loads(html)
        if 'swdata' in data[0]['datasummary']['tables']:
            for key in data[0]['datasummary']['tables']['swdata']['keys']:
                key = key.lower()
                if key in keys:
                    keys[key].append(scraper)
                else:
                    keys[key] = [scraper]
    def lensort(a, b):
        return cmp(len(keys[b]), len(keys[a]))

    for key in sorted(keys.keys(), lensort):
        print len(keys[key]), key, str(keys[key])

def test_parser():
    parser = PDFJournalParser(agency="Dummy agency")
    parser.debug = True
    for url in [ #"http://www.stortinget.no/Global/pdf/postjournal/pj-2011-06-23.pdf",
                "http://www.radhusets-forvaltningstjeneste.oslo.kommune.no/getfile.php/rådhusets%20forvaltningstjeneste%20(RFT)/Intranett%20(RFT)/Dokumenter/Postjournal/11%20November/29112011.pdf",
        ]:
        pdfcontent = scraperwiki.scrape(url)
        parser.preprocess(url,pdfcontent)
        parser.process_pages()

if __name__ == "scraper" or __name__ == '__main__':
    test_parser()
#    fieldlist()

