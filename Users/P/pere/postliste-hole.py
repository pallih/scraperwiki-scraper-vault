# -*- coding: UTF-8 -*-
import scraperwiki
import lxml.html
import datetime
import dateutil.parser
import urllib2
import urlparse

# Start page is the front page, to get it listed as the primary source
scraperwiki.scrape("http://www.hole.kommune.no/postjournaler.173497.no.html")

postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Hole kommune'

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

def expand_id(value, fieldtype, entry):
    year, seqnr = value.split('/')
    year = int(year)
    seqnr = int(seqnr)
    if year < 50:
        year = year + 2000
    if year > 50 and year < 100:
        year = year + 1900
    entry[fieldtype + 'year'] = year
    entry[fieldtype + 'seqnr'] = seqnr
    newvalue = str(year) + '/' + str(seqnr)
    return entry, newvalue

def fetch_postjournal(agency, url, datastore):
#    print "Scraping " + url
    scrapestamputc = datetime.datetime.now()
    html = fetch_url(url)
    root = lxml.html.fromstring(html)
    entry = {
        'agency' : agency,
        'scrapestamputc' : scrapestamputc,
        'scrapedurl' : url,
    }

    fieldmap = {
        u'Tittel på saken'      : 'casedesc',
        u'Tittel på dokumentet' : 'docdesc',
        'Dokumentansvarlig'    : 'saksansvarlig',
        'Hjemmel'     : 'exemption',
        'DokumentID'  : 'journalid',
        'ArkivsakID'  : 'caseid', 
        'Journaldato' : 'recorddate',
        'Brevdato'    : 'docdate',
        #'Journalpostkategori' : 
    }
    doctypemap = { # Valid codes are I, U, X, N, S
        u'Innkommende dokument'                  : 'I',
        u'Innkommende dokument (Gradert)'        : 'I',
        u'Utgående dokument'                     : 'U',
        u'Utgående dokument (Gradert)'           : 'U',
        u'Utgående dokument (Ikke publisert)'    : 'X',
        u'Innkommende dokument (Ikke publisert)' : 'X',
        u'Internt notat (Gradert)'               : 'N',
        u'Internt notat'                         : 'N',
    }
    for span in root.cssselect("div.innsyn-content"):
        #print span.text_content()

        doctype = span.cssselect("h1.header-head")[0].text_content().strip()
        print doctype
        entry['doctype'] = doctypemap[doctype]

        trs = span.cssselect("div.nobox tr")
        for tr in trs:
            field = tr.cssselect("th.header-cell")[0].text_content().strip().replace(":","")
            value = tr.cssselect("td.content-cell")[0].text_content().strip()
            #print "'" + field + "' = " + value
            if field in fieldmap:
                field = fieldmap[field]
                #print "hit"
            if field in ['docdate','recorddate']:
                value = dateutil.parser.parse(value, dayfirst=True).date()
            if field == 'saksansvarlig' and -1 != value.find(','):
                #print value
                names = value.split(",", 1)
                value = names[1].strip() + " " + names[0].strip()
            if field == 'caseid':
                entry, value = expand_id(value, 'case', entry)
            if field == 'journalid':
                entry, value = expand_id(value, 'journal', entry)

            entry[field] = value

    sendinfo = span.cssselect("div.dokmottakere")
    if 0 < len(sendinfo):
        if 'doctype' in entry and entry['doctype'] in ['U', 'X', 'N']:
            field = 'recipient'
        else:
            field = 'sender'
        # Value is "Margrethe Ingeland<br/>Gravfossveien<br/>3360 GEITHUS", should be split in person, addr and zip
        entry[field] = sendinfo[0].text
        brs = sendinfo[0].cssselect("br")
        if 3 == len(brs):
            addr = brs[0].tail + ", " + brs[1].tail
            zip  = brs[2].tail
            entry[field + 'addr'] = addr
            entry[field + 'zip'] = zip
        elif 2 == len(brs):
            addr = brs[0].tail
            zip  = brs[1].tail
            entry[field + 'addr'] = addr
            entry[field + 'zip'] = zip
        elif 1 == len(brs):
            zip  = brs[0].tail
            entry[field + 'zip'] = zip
        elif 0 == len(brs):
            True # Ignore
        else:
            raise ValueError("Unexpected number of address lines")
    print entry
    if 'doctype' in entry:
        entry['casedocseq'] = 0 # Fake value, not sure how to extract the real value
        datastore.append(entry)
    return

def get_journal_day(agency, date, startrow, jurlqueue):
    datestr = str(date) + "T00:00:00"
    url = "http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true&fradato=%s&startrow=%d" % (datestr, startrow)
    print url
    html = fetch_url(url)
    root = lxml.html.fromstring(html)
    ahrefs = root.cssselect("table.inner-max-width tbody tr a")
    for a in ahrefs:
        href = a.attrib['href']
        if -1 != href.find("/wfinnsyn.ashx?response=journalpost_detaljer&journalpostid="):
            jurl = urlparse.urljoin(url, href)
            jurlqueue.append(jurl)

    ahrefs = root.cssselect("table.inner-max-width tfoot tr a")
    for a in ahrefs:
        if 'neste' == a.text_content():
            get_journal_day(agency, date, startrow+10, jurlqueue)

def is_already_scraped(url):
    for sql in ["scrapedurl from swdata where scrapedurl = '" + url + "' limit 1"]:
        try:
            result = scraperwiki.sqlite.select(sql)
            #int sql, " : ", result
            if 0 < len(result) and u'scrapedurl' in result[0]:
                return True
        except:
            print "Exception"
            pass
    return False

def minmax_recorddate(minmax):
    for sql in ["%s(recorddate) as recorddate from swdata" % minmax]:
        try:
            result = scraperwiki.sqlite.select(sql)
            date = dateutil.parser.parse(result[0]['recorddate']).date()
            return date
        except:
            pass
    return None

def scraper():
    html = fetch_url("http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true")
    root = lxml.html.fromstring(html)
    table = root.cssselect("table.inner-max-width")
    #print table[0].text_content()

    lastdate = dateutil.parser.parse(table[0].cssselect("caption")[0].text_content().replace("Postliste den ", ""), dayfirst=True).date()

    maxdate = minmax_recorddate("max")

    if maxdate:
        startdate = maxdate + datetime.timedelta(days=1)
        start = 0
        end = (lastdate-startdate).days + 1
        print maxdate, startdate, start, end
    else:
        startdate = maxdate
        start = 0
        end = 0
    for old in range(start, end):
        date = startdate + datetime.timedelta(days=old)
        print date
        urlqueue = []
        get_journal_day(agency, date, 0, urlqueue)
        datastore = []
        for jurl in urlqueue:
            if not is_already_scraped(jurl):
                res = fetch_postjournal(agency, jurl, datastore)
        if 0 < len(datastore):
            print datastore
            scraperwiki.sqlite.save(unique_keys=['scrapedurl'], data=datastore)
            datastore = []

    mindate = minmax_recorddate("min")

    # Only three months back
    return

    if mindate:
        startdate = mindate - datetime.timedelta(days=1)
        start = 0
        end = -60
        print mindate, startdate, start, end
    else:
        return
    for old in range(start, end, -1):
        date = startdate + datetime.timedelta(days=old)
        print date
        urlqueue = []
        get_journal_day(agency, date, 0, urlqueue)
        datastore = []
        for jurl in urlqueue:
            if not is_already_scraped(jurl):
                res = fetch_postjournal(agency, jurl, datastore)
        if 0 < len(datastore):
            print datastore
            scraperwiki.sqlite.save(unique_keys=['scrapedurl'], data=datastore)
            datastore = []

#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true&fradato=2012-06-15T00:00:00
#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_detaljer&journalpostid=2012005569&
#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=arkivsak_detaljer&arkivsakid=2006002016&

if __name__ == "scraper":
    scraper()
else:
    print "Not called as scraper"# -*- coding: UTF-8 -*-
import scraperwiki
import lxml.html
import datetime
import dateutil.parser
import urllib2
import urlparse

# Start page is the front page, to get it listed as the primary source
scraperwiki.scrape("http://www.hole.kommune.no/postjournaler.173497.no.html")

postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Hole kommune'

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

def expand_id(value, fieldtype, entry):
    year, seqnr = value.split('/')
    year = int(year)
    seqnr = int(seqnr)
    if year < 50:
        year = year + 2000
    if year > 50 and year < 100:
        year = year + 1900
    entry[fieldtype + 'year'] = year
    entry[fieldtype + 'seqnr'] = seqnr
    newvalue = str(year) + '/' + str(seqnr)
    return entry, newvalue

def fetch_postjournal(agency, url, datastore):
#    print "Scraping " + url
    scrapestamputc = datetime.datetime.now()
    html = fetch_url(url)
    root = lxml.html.fromstring(html)
    entry = {
        'agency' : agency,
        'scrapestamputc' : scrapestamputc,
        'scrapedurl' : url,
    }

    fieldmap = {
        u'Tittel på saken'      : 'casedesc',
        u'Tittel på dokumentet' : 'docdesc',
        'Dokumentansvarlig'    : 'saksansvarlig',
        'Hjemmel'     : 'exemption',
        'DokumentID'  : 'journalid',
        'ArkivsakID'  : 'caseid', 
        'Journaldato' : 'recorddate',
        'Brevdato'    : 'docdate',
        #'Journalpostkategori' : 
    }
    doctypemap = { # Valid codes are I, U, X, N, S
        u'Innkommende dokument'                  : 'I',
        u'Innkommende dokument (Gradert)'        : 'I',
        u'Utgående dokument'                     : 'U',
        u'Utgående dokument (Gradert)'           : 'U',
        u'Utgående dokument (Ikke publisert)'    : 'X',
        u'Innkommende dokument (Ikke publisert)' : 'X',
        u'Internt notat (Gradert)'               : 'N',
        u'Internt notat'                         : 'N',
    }
    for span in root.cssselect("div.innsyn-content"):
        #print span.text_content()

        doctype = span.cssselect("h1.header-head")[0].text_content().strip()
        print doctype
        entry['doctype'] = doctypemap[doctype]

        trs = span.cssselect("div.nobox tr")
        for tr in trs:
            field = tr.cssselect("th.header-cell")[0].text_content().strip().replace(":","")
            value = tr.cssselect("td.content-cell")[0].text_content().strip()
            #print "'" + field + "' = " + value
            if field in fieldmap:
                field = fieldmap[field]
                #print "hit"
            if field in ['docdate','recorddate']:
                value = dateutil.parser.parse(value, dayfirst=True).date()
            if field == 'saksansvarlig' and -1 != value.find(','):
                #print value
                names = value.split(",", 1)
                value = names[1].strip() + " " + names[0].strip()
            if field == 'caseid':
                entry, value = expand_id(value, 'case', entry)
            if field == 'journalid':
                entry, value = expand_id(value, 'journal', entry)

            entry[field] = value

    sendinfo = span.cssselect("div.dokmottakere")
    if 0 < len(sendinfo):
        if 'doctype' in entry and entry['doctype'] in ['U', 'X', 'N']:
            field = 'recipient'
        else:
            field = 'sender'
        # Value is "Margrethe Ingeland<br/>Gravfossveien<br/>3360 GEITHUS", should be split in person, addr and zip
        entry[field] = sendinfo[0].text
        brs = sendinfo[0].cssselect("br")
        if 3 == len(brs):
            addr = brs[0].tail + ", " + brs[1].tail
            zip  = brs[2].tail
            entry[field + 'addr'] = addr
            entry[field + 'zip'] = zip
        elif 2 == len(brs):
            addr = brs[0].tail
            zip  = brs[1].tail
            entry[field + 'addr'] = addr
            entry[field + 'zip'] = zip
        elif 1 == len(brs):
            zip  = brs[0].tail
            entry[field + 'zip'] = zip
        elif 0 == len(brs):
            True # Ignore
        else:
            raise ValueError("Unexpected number of address lines")
    print entry
    if 'doctype' in entry:
        entry['casedocseq'] = 0 # Fake value, not sure how to extract the real value
        datastore.append(entry)
    return

def get_journal_day(agency, date, startrow, jurlqueue):
    datestr = str(date) + "T00:00:00"
    url = "http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true&fradato=%s&startrow=%d" % (datestr, startrow)
    print url
    html = fetch_url(url)
    root = lxml.html.fromstring(html)
    ahrefs = root.cssselect("table.inner-max-width tbody tr a")
    for a in ahrefs:
        href = a.attrib['href']
        if -1 != href.find("/wfinnsyn.ashx?response=journalpost_detaljer&journalpostid="):
            jurl = urlparse.urljoin(url, href)
            jurlqueue.append(jurl)

    ahrefs = root.cssselect("table.inner-max-width tfoot tr a")
    for a in ahrefs:
        if 'neste' == a.text_content():
            get_journal_day(agency, date, startrow+10, jurlqueue)

def is_already_scraped(url):
    for sql in ["scrapedurl from swdata where scrapedurl = '" + url + "' limit 1"]:
        try:
            result = scraperwiki.sqlite.select(sql)
            #int sql, " : ", result
            if 0 < len(result) and u'scrapedurl' in result[0]:
                return True
        except:
            print "Exception"
            pass
    return False

def minmax_recorddate(minmax):
    for sql in ["%s(recorddate) as recorddate from swdata" % minmax]:
        try:
            result = scraperwiki.sqlite.select(sql)
            date = dateutil.parser.parse(result[0]['recorddate']).date()
            return date
        except:
            pass
    return None

def scraper():
    html = fetch_url("http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true")
    root = lxml.html.fromstring(html)
    table = root.cssselect("table.inner-max-width")
    #print table[0].text_content()

    lastdate = dateutil.parser.parse(table[0].cssselect("caption")[0].text_content().replace("Postliste den ", ""), dayfirst=True).date()

    maxdate = minmax_recorddate("max")

    if maxdate:
        startdate = maxdate + datetime.timedelta(days=1)
        start = 0
        end = (lastdate-startdate).days + 1
        print maxdate, startdate, start, end
    else:
        startdate = maxdate
        start = 0
        end = 0
    for old in range(start, end):
        date = startdate + datetime.timedelta(days=old)
        print date
        urlqueue = []
        get_journal_day(agency, date, 0, urlqueue)
        datastore = []
        for jurl in urlqueue:
            if not is_already_scraped(jurl):
                res = fetch_postjournal(agency, jurl, datastore)
        if 0 < len(datastore):
            print datastore
            scraperwiki.sqlite.save(unique_keys=['scrapedurl'], data=datastore)
            datastore = []

    mindate = minmax_recorddate("min")

    # Only three months back
    return

    if mindate:
        startdate = mindate - datetime.timedelta(days=1)
        start = 0
        end = -60
        print mindate, startdate, start, end
    else:
        return
    for old in range(start, end, -1):
        date = startdate + datetime.timedelta(days=old)
        print date
        urlqueue = []
        get_journal_day(agency, date, 0, urlqueue)
        datastore = []
        for jurl in urlqueue:
            if not is_already_scraped(jurl):
                res = fetch_postjournal(agency, jurl, datastore)
        if 0 < len(datastore):
            print datastore
            scraperwiki.sqlite.save(unique_keys=['scrapedurl'], data=datastore)
            datastore = []

#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_postliste&showresults=true&fradato=2012-06-15T00:00:00
#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=journalpost_detaljer&journalpostid=2012005569&
#GET http://innsyn.hole.kommune.no/wfinnsyn.ashx?response=arkivsak_detaljer&arkivsakid=2006002016&

if __name__ == "scraper":
    scraper()
else:
    print "Not called as scraper"