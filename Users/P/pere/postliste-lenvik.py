# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import lxml.html
import re
import dateutil.parser
from dateutil.relativedelta import relativedelta
import datetime
import urlparse

agency = "Lenvik kommune"

# Point scraperwiki GUI to the start page
scraperwiki.scrape("http://webway.lenvik.kommune.no/postjournal")

postlistelib=scraperwiki.swimport('postliste-python-lib')
parser = postlistelib.JournalParser(agency=agency)

def saver(unique_keys, data):
#    return
    #print "Not saving data"
    scraperwiki.sqlite.save(unique_keys, data)

def expand_year(year):
    year = int(year)
    if year > 50:
        year = year + 1900
    else:
        year = year + 2000
    return year

#            <tr class=yang>
#              <td>13/00563-001</td>
#              <td>04.03.2013</td>
#              <td style="text-align:center;">
#                <div title="Inngående">I</div>
#              </td>
#              <td>Flytting av VPN-tunell </td>
#                  <td>EVRY AS</td>
#              <td>Jan-Eirik Nordahl</td>
#                  <td>
#                        <a href="/dokumentbestilling?jpid=13003566" title="Klikk for å bestille innsyn">Bestill</a>
#                  </td>
#                  <td></td>
#
#            </tr>
#

def fetch_postjournal_day(parser, url, html, saver):
    root = lxml.html.fromstring(html.decode('utf-8'))

    recorddate = None
    for div in root.cssselect('div'):
        divcontent = div.text_content()
        if 0 == divcontent.find("Offentlig postjournal for "):
            recorddate = dateutil.parser.parse(divcontent.replace("Offentlig postjournal for ",""), dayfirst=True)
    print recorddate

    # Make sure we save the entire URL or nothing at all
    datastore = []
    for tr in root.cssselect('tr.yang'):
        tds = tr.cssselect("td")
        docidstr = tds[0].text_content().strip()
        docdate = tds[1].text_content().strip()
        doctype = tds[2].text_content().strip()
        docdesc = tds[3].text_content().strip()
        fratil = tds[4].text_content().strip()
        saksbehandler = tds[5].text_content().strip()
        if -1 != tds[6].text_content().find("Bestill"):
            exemption = None
        else:
            exemption = tds[6].text_content().strip()

        docdate = dateutil.parser.parse(docdate, dayfirst=True)

#        print doctype, docdesc
        if not parser.is_valid_doctype(doctype):
            doctype = {
                '' : '?',
                }[doctype]
        if parser.is_sender_doctype(doctype):
            fratilfield = 'sender'
        elif parser.is_recipient_doctype(doctype):
            fratilfield = 'recipient'

        caseyear, caseseqnr = docidstr.split("/")
        caseyear = expand_year(caseyear)
        caseseqnr, casedocseq = caseseqnr.split("-")
        caseid = "%d/%d" % (int(caseyear), int(caseseqnr))

        data = {
            'agency' : parser.agency,
            'recorddate' : recorddate.date(),
            'docdate' : docdate.date(),
            'docdesc' : docdesc,
            'casedesc' : docdesc, # FIXME fake value

            'caseyear' : int(caseyear),
            'caseseqnr' : int(caseseqnr),
            'casedocseq' : int(casedocseq),
            'caseid' : caseid,
            'doctype' : doctype,

#        'journalseqnr' : int(journalseqnr),
#        'journalyear' : int(journalyear),
#        'journalid' : journalid,
            fratilfield : fratil,

            'saksbehandler' : saksbehandler,
#        'saksansvarlig' : saksansvarlig.strip(),
#        'saksansvarligenhet' : saksansvarligenhet.strip(),

            'docidstr' : docidstr,
#        'laapenr' : laapenr,
            'exemption' : exemption,

            'scrapedurl' : url,
            'scrapestamputc' : datetime.datetime.now()
            }

#        print data
        parser.verify_entry(data)
        datastore.append(data)

    seenurl = {}
    # Find next URL.  There are two on each page.
    for ahref in root.cssselect('a.next_page'):
        if 0 == ahref.text_content().find('Neste'):
            nexturl = urlparse.urljoin(url, ahref.attrib['href'])
            if nexturl not in seenurl:
                seenurl[nexturl] = True;
                print 'Fetching ' + nexturl
                html = postlistelib.fetch_url_harder(nexturl)
                mysaver = lambda unique_keys, data: datastore.extend(data)
                fetch_postjournal_day(parser=parser, url=nexturl, html=html,
                                      saver=mysaver)

    saver(unique_keys=['docidstr'], data=datastore)

def date2url(date):
    return 'http://webway.lenvik.kommune.no/?date=%s' % date

def gen_date_urls(urllist, startdate, step, count):
    d = dateutil.parser.parse(startdate, dayfirst=False)
    for n in xrange(1, step*(count+1), step):
        next = (d + relativedelta(days=n)).strftime("%Y-%m-%d")
        urllist.append(date2url(next))

urllist = []
today = datetime.date.today()
try:
    first = scraperwiki.sqlite.select("min(recorddate) as min from swdata")[0]['min']
    last = scraperwiki.sqlite.select("max(recorddate) as max from swdata")[0]['max']
except:
    last = (today + relativedelta(days=-14)).strftime("%Y-%m-%d")
    first = None

print first, last

# Parse back in time
if first is not None:
    gen_date_urls(urllist, first, -1, 100)

# Parse forward in time
if last is not None:
    gen_date_urls(urllist, last, 1, 3)

for dayurl in urllist:
    print 'Fetching ' + dayurl
    html = postlistelib.fetch_url_harder(dayurl)
    fetch_postjournal_day(parser=parser, url=dayurl, html=html, saver=saver)

# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import lxml.html
import re
import dateutil.parser
from dateutil.relativedelta import relativedelta
import datetime
import urlparse

agency = "Lenvik kommune"

# Point scraperwiki GUI to the start page
scraperwiki.scrape("http://webway.lenvik.kommune.no/postjournal")

postlistelib=scraperwiki.swimport('postliste-python-lib')
parser = postlistelib.JournalParser(agency=agency)

def saver(unique_keys, data):
#    return
    #print "Not saving data"
    scraperwiki.sqlite.save(unique_keys, data)

def expand_year(year):
    year = int(year)
    if year > 50:
        year = year + 1900
    else:
        year = year + 2000
    return year

#            <tr class=yang>
#              <td>13/00563-001</td>
#              <td>04.03.2013</td>
#              <td style="text-align:center;">
#                <div title="Inngående">I</div>
#              </td>
#              <td>Flytting av VPN-tunell </td>
#                  <td>EVRY AS</td>
#              <td>Jan-Eirik Nordahl</td>
#                  <td>
#                        <a href="/dokumentbestilling?jpid=13003566" title="Klikk for å bestille innsyn">Bestill</a>
#                  </td>
#                  <td></td>
#
#            </tr>
#

def fetch_postjournal_day(parser, url, html, saver):
    root = lxml.html.fromstring(html.decode('utf-8'))

    recorddate = None
    for div in root.cssselect('div'):
        divcontent = div.text_content()
        if 0 == divcontent.find("Offentlig postjournal for "):
            recorddate = dateutil.parser.parse(divcontent.replace("Offentlig postjournal for ",""), dayfirst=True)
    print recorddate

    # Make sure we save the entire URL or nothing at all
    datastore = []
    for tr in root.cssselect('tr.yang'):
        tds = tr.cssselect("td")
        docidstr = tds[0].text_content().strip()
        docdate = tds[1].text_content().strip()
        doctype = tds[2].text_content().strip()
        docdesc = tds[3].text_content().strip()
        fratil = tds[4].text_content().strip()
        saksbehandler = tds[5].text_content().strip()
        if -1 != tds[6].text_content().find("Bestill"):
            exemption = None
        else:
            exemption = tds[6].text_content().strip()

        docdate = dateutil.parser.parse(docdate, dayfirst=True)

#        print doctype, docdesc
        if not parser.is_valid_doctype(doctype):
            doctype = {
                '' : '?',
                }[doctype]
        if parser.is_sender_doctype(doctype):
            fratilfield = 'sender'
        elif parser.is_recipient_doctype(doctype):
            fratilfield = 'recipient'

        caseyear, caseseqnr = docidstr.split("/")
        caseyear = expand_year(caseyear)
        caseseqnr, casedocseq = caseseqnr.split("-")
        caseid = "%d/%d" % (int(caseyear), int(caseseqnr))

        data = {
            'agency' : parser.agency,
            'recorddate' : recorddate.date(),
            'docdate' : docdate.date(),
            'docdesc' : docdesc,
            'casedesc' : docdesc, # FIXME fake value

            'caseyear' : int(caseyear),
            'caseseqnr' : int(caseseqnr),
            'casedocseq' : int(casedocseq),
            'caseid' : caseid,
            'doctype' : doctype,

#        'journalseqnr' : int(journalseqnr),
#        'journalyear' : int(journalyear),
#        'journalid' : journalid,
            fratilfield : fratil,

            'saksbehandler' : saksbehandler,
#        'saksansvarlig' : saksansvarlig.strip(),
#        'saksansvarligenhet' : saksansvarligenhet.strip(),

            'docidstr' : docidstr,
#        'laapenr' : laapenr,
            'exemption' : exemption,

            'scrapedurl' : url,
            'scrapestamputc' : datetime.datetime.now()
            }

#        print data
        parser.verify_entry(data)
        datastore.append(data)

    seenurl = {}
    # Find next URL.  There are two on each page.
    for ahref in root.cssselect('a.next_page'):
        if 0 == ahref.text_content().find('Neste'):
            nexturl = urlparse.urljoin(url, ahref.attrib['href'])
            if nexturl not in seenurl:
                seenurl[nexturl] = True;
                print 'Fetching ' + nexturl
                html = postlistelib.fetch_url_harder(nexturl)
                mysaver = lambda unique_keys, data: datastore.extend(data)
                fetch_postjournal_day(parser=parser, url=nexturl, html=html,
                                      saver=mysaver)

    saver(unique_keys=['docidstr'], data=datastore)

def date2url(date):
    return 'http://webway.lenvik.kommune.no/?date=%s' % date

def gen_date_urls(urllist, startdate, step, count):
    d = dateutil.parser.parse(startdate, dayfirst=False)
    for n in xrange(1, step*(count+1), step):
        next = (d + relativedelta(days=n)).strftime("%Y-%m-%d")
        urllist.append(date2url(next))

urllist = []
today = datetime.date.today()
try:
    first = scraperwiki.sqlite.select("min(recorddate) as min from swdata")[0]['min']
    last = scraperwiki.sqlite.select("max(recorddate) as max from swdata")[0]['max']
except:
    last = (today + relativedelta(days=-14)).strftime("%Y-%m-%d")
    first = None

print first, last

# Parse back in time
if first is not None:
    gen_date_urls(urllist, first, -1, 100)

# Parse forward in time
if last is not None:
    gen_date_urls(urllist, last, 1, 3)

for dayurl in urllist:
    print 'Fetching ' + dayurl
    html = postlistelib.fetch_url_harder(dayurl)
    fetch_postjournal_day(parser=parser, url=dayurl, html=html, saver=saver)

