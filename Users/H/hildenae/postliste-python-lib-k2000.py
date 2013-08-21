# -*- coding: UTF-8 -*-
#
# Python library for parsing public post journals (postlister) in Norway. Format K2000
#
# Google search to find more: "postliste k2post.nsf"

'''
K2000 e-Sak er IBMs journal-/arkivsystem med nytt brukergrensesnitt og nye funksjoner. K2000 e-Sak er en videreutvikling av IBMs journal-/arkivsystem Kontor 2000.
K2000 eSak var IBMs system inntil 01.01.2005 da enheten med ansvar for offentlige løsninger ble kjøpt av EDB Business Partner A/S.
234 kommuner.
Referanser:
hs.iheroy.no/fileadmin/Nyheter_K2000_v_5_3.pdf
esa-hjelp.no/files/Administrator.pdf
http://lkpub01.lunner.kommune.no:8080/k2000/k2post.nsf
http://217.18.200.82:81/k2000/k2post.nsf/
http://www.vestre-toten.kommune.no/k2000/k2post.nsf/
https://sametime.hemne.kommune.no/k2000/k2post.nsf
http://mobil.iktin.no/Grong/K2000/k2post.nsf/
http://politiker.kongsberg.kommune.no/edb_sak_arkiv/polpub/k2post.nsf

??? http://www.ballangen.kommune.no/artikler/postlister

http://www-05.ibm.com/no/newworld/2004/2/art7.html
# https://scraperwiki.com/scrapers/postliste-ballangen/edit/
konsberg: http://politiker.kongsberg.kommune.no/edb_sak_arkiv/polpub/k2post.nsf/frmShowMailBySpecifiedDate?OpenForm&Date=20120629
gjøvik:   http://217.18.200.82:81/k2000/k2post.nsf/frmShowMailBySpecifiedDate?OpenForm&Date=20120629
http://wiki.nuug.no/grupper/offentliginnsyn
 `swdata` (
`exemption` text, 
`sender` text, FRA
`casedesc` text, 
`recorddate` text, 
`casedocseq` integer, 
`agency` text, 
`doctype` text, Parse ARKIVSAKNUMMER for inngående/utgående/annet
`journalyear` integer, ?? siste to siffer i LØPENR eller årsatt i DATERT?
`docdesc` text, 
`scrapestamputc` text, 
`caseseqnr` integer, 
`scrapedurl` text, 
`docdate` text, 
`caseid` text, 
`accesscode` text, 
`journalid` text, 
`journalseqnr` integer, 
`caseyear` integer, 
`recipient` text) TIL:


'''

import scraperwiki # retriving html
import lxml.html # parsing html
import dateutil.parser # parsing Datert
import re # parsing arkivsaksnr
utils=scraperwiki.swimport('hildenae_utils') # for caching + pretty-print
import time
from datetime import date # fro getting current year/month
import resource # cpu measurements

def expand_year(year):
    year = int(year)
    if year > 50:
        year = year + 1900
    else:
        year = year + 2000
    return year

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

    def __init__(self, agency, debug=False):
        self.agency = agency
        self.debug = debug

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
            raise ValueError("Invalid doctype %s" % entry['doctype'])

        if -1 != entry['caseid'].find('-'):
            raise ValueError("Field caseid should not include dash: " + entry['caseid'])


        # Seen in http://home.nuug.no/~pere/nrk-postjournal/Offentlig%20journal%20NRK%200101_15012011.pdf
        if 'sender' in entry and -1 != entry['sender'].find("Side: "):
            raise ValueError("Field sender got page number, not real content")

class K2000JournalParser(JournalParser):
    pagetable = "unparsedpages"
    brokenpagetable = "brokenpages"
    breakonfailure = True
    time = time.time()
    errors = []
    def __init__(self, baseurl, agency, debug=False, firstYear=-1, firstMonth=-1, limit = 10):
        JournalParser.__init__(self, agency=agency,debug=debug)
        if (firstMonth != -1 and firstYear == -1): raise Exception("Cannot specicy firstMonth without firstYear")
        if (firstYear != -1 and firstMonth == -1): firstMonth = 1
        self.firstMonth = firstMonth
        self.firstYear = firstYear
        self.baseURL = baseurl
        self.limit = limit
        self.recordURL = "%s/lupMailByYearAndMonthAndDate/%%s?OpenDocument&frame=no" % baseurl
        self.dayURL = "%s/frmShowMailBySpecifiedDate?OpenForm&Date=%%s" % baseurl
        self.startURL = "%s/%s" % (self.baseURL, "frmMailCalendar")
        self.calendarURL = "%s/frmMailCalendar?OpenForm&Year=%%d&Month=%%d" % baseurl

    def report_errors(self):
        if 0 < len(self.errors):
            print "Errors:"
            for e in self.errors:
                print e
            exit(1)
        elif self.debug: print "No errors recorded."
    
    def cpu_spent(self):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

    def exit_if_no_cpu_left(self):
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
        spent = self.cpu_spent()
        if self.debug: print "CPU time spent %f0.2 of %f0.2 (%f0.2)" % (spent, soft, hard)
        if soft < spent:
            self.report_errors()
            print "Running out of CPU, exiting."
            exit(5)

    def limiter(self):
        last_time = self.time
        now = time.time()
        delta = now - last_time;
        self.time = now
        if delta < self.limit:
            if self.debug: print "Sleeping %f seconds" % (self.limit - delta)
            time.sleep((self.limit - delta))
        elif self.debug: print "Not sleeping (%d)" % delta

    def scrapeRecord(self, id):
        self.exit_if_no_cpu_left()
        # Parse then do x with record with id
        url = self.recordURL % id
        if self.debug: print "Scraping ID %s (%s)" % (id, url)
        html = utils.findInCache(url)
        if html is None:
            self.limiter()
            html = scraperwiki.scrape(url)
            utils.putInCache(url, html)
        root = lxml.html.fromstring(html)

        record = {}
        record["agency"] = self.agency
        record["scrapedurl"] = url
        record["k2k_id"] = id
        bar = root.cssselect("td.tdNavigate")
        if len(bar) != 1: 
            e("More than one tdNavigate on record " % id)

        text = bar[0].text_content().replace(u"\u00A0", " ") # Remove nbsp

        matchObj = re.match(r'.*Postliste\s*(\d{2}/\d{2}/\d{4})\s*$', text, re.DOTALL)
        if matchObj:
            record['recorddate'] = dateutil.parser.parse(matchObj.group(1), dayfirst=True).date()
        else:
            e("Could not find recorddate on record %s" % url)

        # Retrive all information from page
        prevRecord = None # used for handling multiline values
        for el in root.cssselect("table tr"):
            #print lxml.html.tostring(el)
            c = el.getchildren();
            #print ">%s<" % c[0].text
            if c[0].text is not None:
                k = c[0].text.strip()
                v = ''
                if(len(c) > 1):
                    v = c[1].text.strip()

                if k == 'Sakstittel:'      : 
                    record['casedesc'] = v; continue
                elif k == 'Arkivsaksnr.:'  : 
                    record['arkivsaksnr'] = v; continue
                elif k == 'Datert:'        : 
                    record['recorddate'] = dateutil.parser.parse(v, dayfirst=True).date(); continue
                elif k == 'Arkivkode:'     : 
                    record['arkivkode'] = v; continue
                elif k == 'Saksansvarlig:' : 
                    # ref saksbehandler nedenfor
                    #'saksansvarlig': 'TT//AHF'
                    #'saksansvarlig': 'LOS//REB'
                    #'saksansvarlig': 'RM/TK/TRHODEN'
                    record['saksansvarlig'] = v; continue
                elif k == 'Saksbehandler:' :
                    # ref saksansvarlig ovenfor
                    #'saksbehandler': 'Liv Mette Haga(TT/)'
                    #'saksbehandler': 'Anette Wad Garmo(LOS/)'
                    #'saksbehandler': 'Trygve Rhoden(RM/TK)'
                    record['saksbehandler'] = v; continue
                    #saksbehandler = queue.popleft().replace("Saksbehandler:","").strip()
                    #saksansvarlig, bar = saksbehandler.split(" (")
                    #saksansvarligenhet, foo = bar.split(")")
                elif k == 'Fra:'           : 
                    record['sender'] = v; continue
                elif k == 'Til:'           : 
                    if 'recipient' not in record:
                        record['recipient'] = v
                    else: # Multiple Til
                        record['recipient'] = record['recipient'] + ", " + v;
                    continue
                elif k == 'Mottaker:'      : 
                    if 'mottaker' in record: raise Error("Overwriting key")
                    record['mottaker'] = c[1].text; continue
                elif k == 'Gradering:'     : record['exemption'] = v; continue
                elif k == 'Vedlegg:'       : record['vedlegg'] = v; continue
                elif k == u'Løpenr.:'      : record['laapenr'] = v; continue
                elif k == 'Journalenhet:'  : record['journalenhet'] = v; continue
                elif k == u'Svar på lnr.:' : record['answer_to_laapenr'] = v; continue
                elif k == u'Navn:'         : record['received_by'] = v; continue
                elif k == 'Innhold:'       : 
                    record['docdesc'] = v; prevRecord = "docdesc";
                    continue
            
                if prevRecord == 'docdesc' : # Support twoline Innhold
                    record['docdesc'] = record['docdesc'] + "\n" + v
                    prevRecord = None;
                    continue

                if k != "": # By this time all know keys should have been parsed an continue-ed
                    print u"Unknown, not-empty key: '%s' (URL: %s)(%s)" % (c[0].text, url, utils.dump(c[0].text))
                    raise  Exception("Error in library, source or not supported: Unknown, not-empty key: <see last output>")
                
                assert(len(c) <= 2), "There should not be more than two cells"
                
                if(len(c) > 1 and v != ''): # key might be empty but have value
                    print u"Unknown, not-empty value: '%s' (URL: %s) (%s)" % (c[1].text, url, utils.dump(c[1].text))
                    raise  Exception("Error in library, source or not supported: Found data we could not save: <see last output>")

        # Parse Arkivsaknr into caseyear, caseseqnr, casedocseq, doctype and caseid
        record['caseyear'] = 0
        record['caseseqnr'] = 0
        record['casedocseq'] = 0
        record['doctype'] = '?'
        record['caseid'] = 'unknown'
        matchObj = re.match("(\d+)/(\d+)\s*-\s*(\d+)\s*(.+)$", record['arkivsaksnr'], re.M|re.I)
        if matchObj:
            record['caseyear'] = matchObj.group(1)
            record['caseseqnr'] = matchObj.group(2)
            record['casedocseq'] = matchObj.group(3)

            #Dokumenttype I/U er erstattet med "Inngående/utgående post" i visningsbildene.
            #Dokumenttype N/X/S er erstattet med "Notat"/"Internt notat"/"Saksframlegg"
            if   matchObj.group(4).find(u"Inngående post") != -1: record['doctype'] = 'I'
            elif matchObj.group(4).find(u"Utgående post")  != -1: record['doctype'] = 'U'
            elif matchObj.group(4).find(u"Internt notat")  != -1: record['doctype'] = 'X'
            elif matchObj.group(4).find(u"Notat")          != -1: record['doctype'] = 'N'
            elif matchObj.group(4).find(u"Saksframlegg")   != -1: record['doctype'] = 'S'
            else: record['doctype'] = matchObj.group(4)

            record['caseyear'] = expand_year(record['caseyear'])
            record['caseid'] = str(record['caseyear']) + "/" + str(record['caseseqnr'])
        else:
            e(u"error: invalid Arkivsaksnr (%s) on record %s " %(record['arkivsaksnr'], url))
            matchObj = re.match( r'(\d+)/(\d+)\s*-', record['arkivsaksnr'], re.M|re.I)
            #print matchObj 
            if matchObj:
                caseyear = expand_year(matchObj.group(1))
                caseseqnr = matchObj.group(2)
                caseid = str(caseyear) + "/" + str(caseseqnr)

        # Parse Løpenr into journalseqnr, journalyear and journalid
        journalseqnr = 0
        journalyear = 0
        journalid = 'unknown'
        if -1 != record['laapenr'].find('/') and "/" != record['laapenr']: # Avoid broken/empty values
            journalseqnr, journalyear = record['laapenr'].split("/")
            record['journalseqnr'] = int(journalseqnr)
            record['journalyear']  = int(expand_year(journalyear))
            record['journalid']    = str(journalyear) + "/" + str(journalseqnr)
        else:
            e(u"error: invalid Løpenr (%s) on record %s " %(record['laapenr'], url))

        utils.pretty(record)
        JournalParser.verify_entry(self, record)

    def scrapeDaypage(self, date):
        # Return list of record ID's for date (YYYYMMDD)
        url = self.dayURL % date
        if self.debug: print "Scraping for IDs at %s" %url
        html = utils.findInCache(url, verbose=self.debug)
        if html is None:
            self.limiter()
            html = scraperwiki.scrape(url)
            utils.putInCache(url, html, verbose=self.debug)
        root = lxml.html.fromstring(html)
        ids = []
        idregx = r'.*viewAttachmentsMail/([A-Z0-9_]*)\?open.*'
        for el in root.cssselect("blockquote table:nth-child(1) a"):     
            matchObj = re.match(idregx, el.attrib['href'])
            if matchObj:
                ids.append(matchObj.group(1))
            else:
                e("Could not find record ID (%s)" % el.attrib['href'])
        if len(ids) == 0:
            raise  Exception("Error in library, source or useage. Scraped empty day. : %s" % url)
        return ids

    def scrapeCalendar(self, year, month):
        # Return list of days w. journals for year and month
        url = self.calendarURL % (year, month)
        if self.debug: print "Scraping for valid days %s" % url
        html = utils.findInCache(url)
        if html is None:
            self.limiter()
            html = scraperwiki.scrape(url)
            utils.putInCache(url, html)
        root = lxml.html.fromstring(html)
        dayList = root.cssselect('form input[type="hidden"][name^="Day"][value="1"]')

        if(len(dayList) == 1 and dayList[0].attrib['name'] == 'Day@ERROR'):
            return None # 0 valid days this month
        validdays = []
        for i in dayList:
            validdays.append(int(i.attrib['name'].replace("Day", "")))
        validdays.sort()
        return validdays

    def determineStartMonthAndYear(self):
        #already supplied values trumph all
        if self.firstYear != -1 and self.firstMonth != -1:
            if self.debug: print "Using supplied firstYear and firstMonth"
            return (self.firstYear, self.firstMonth)

        if self.firstMonth == -1: # month not defined
            observedFirstMonth = scraperwiki.sqlite.get_var("observedFirstMonth",-1)
            if observedFirstMonth != -1:
                if self.debug: print "Using observedFirstMonth (%d)" % observedFirstMonth
                self.firstMonth = observedFirstMonth # update firstmonth with observed month
            else:
                if self.debug: print "Using supplied january for unknown month, have not observed better"
                self.firstMonth = 1 # update firstmonth with januay

        
        if self.firstYear == -1: # year not defined
            observedFirstYear = scraperwiki.sqlite.get_var("observedFirstYear",-1)        
            if observedFirstYear != -1: # we have a observed year
                if self.debug: print "Using observedFirstYear (%d)" % observedFirstYear
                self.firstYear = observedFirstYear
            else: # we have no year must find earliest possible
                if self.debug: print "Looking for startyear in HTML"
                html = utils.findInCache(self.startURL)
                if html is None:
                    #self.limiter() # no, don't limit this
                    html = scraperwiki.scrape(self.startURL)
                    utils.putInCache(self.startURL, html)
                root = lxml.html.fromstring(html)
                for option in root.cssselect('select[name="tbSelYear"] option'):
                    # update firstYear if it is unset (-1) or higer than the value we found
                    if self.firstYear == -1 or self.firstYear > int(option.attrib['value']): self.firstYear = int(option.attrib['value'])
                # we now have a firstyear
                if self.debug: print "Ended up with firstyear (%d)" % self.firstYear

    def is_already_scraped(self, url):
        # Ignore entries were sender and recipient is the result of a broken parser (before 2012-05-25)
        for sql in ["scrapedurl, sender, recipient from swdata where scrapedurl = '" + url + "' " +
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

    def scrapeAll(self):
        
        if self.debug: print "Scraping K2000 from %s at %s" % (self.agency, self.baseURL)

        lastMonth = date.today().month
        lastYear = date.today().year
        self.determineStartMonthAndYear()        
        if self.debug: print "Scraping from %d-%d to %d-%d" % (self.firstYear,self.firstMonth,lastYear,lastMonth)
        observedFirstYear = scraperwiki.sqlite.get_var("observedFirstYear",-1)   
        
        second_year = False
        firstMonth = self.firstMonth
        tmpMonth = 12
        foundSomeDays = False;
        for year in range(self.firstYear, lastYear+1):
            if second_year: firstMonth = 1 # we have completed a year, back to january
            else: second_year = True
            if year == lastYear: tmpMonth = lastMonth # we are on the last year, don't scrape next month!
            for month in range(firstMonth, tmpMonth+1):
                days = self.scrapeCalendar(year, month)
                if self.debug: print "Valid days for %d-%d: " % (year,month),; utils.pretty(days)
                if days is not None:
                    if scraperwiki.sqlite.get_var("observedFirstMonth",-1) == -1:
                        if self.debug: print "Set observedFirstMonth to %d: "  % month
                        scraperwiki.sqlite.save_var("observedFirstMonth", month)
                    if scraperwiki.sqlite.get_var("observedFirstYear",-1) == -1:
                        if self.debug: print "Set observedFirstYear to %d: "  % year
                        scraperwiki.sqlite.save_var("observedFirstYear", year)
                    for day in days:
                        case_ids = self.scrapeDaypage("%d%0.2d%0.2d" % (year,month,day))
                        if self.debug: print "Valid IDs for %d-%d-%d: "  % (year,month,day),; utils.pretty(case_ids)
                        for case_id in case_ids:
                            self.scrapeRecord(case_id)
                else:
                    if self.debug: print "Found no days for %d-%d: "  % (year,month)
                
            #end of year


if __name__ == "scraper":
    #TODO: Sjekk om Til: inneholder komma før sammenslåing
    #TODO: Svar på lnr ?
    #TODO: Navn ?

    #errors = []
    parser = K2000JournalParser("http://politiker.kongsberg.kommune.no/edb_sak_arkiv/PolPub/k2post.nsf", "Kongsberg kommune", debug=True, limit=3)
    parser.scrapeAll()

    parser.report_errors()    
    #print parser.scrapeCalendar(year=2012, month=6)
    #print parser.scrapeDaypage("20080706")
    #records = (
    #    "C125791E003FB9FAC1257A320047E0AE",  # multiline innhold
    #    "C125791E003FB9FAC1257A320047DFA3",
    #)
    #records = parser.scrapeDaypage("20120701")

    #for record in records:
    #    parser.scrapeRecord(record)
    