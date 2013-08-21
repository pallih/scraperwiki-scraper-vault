# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import lxml.html
import re
import dateutil.parser
from collections import deque
import datetime
from dateutil.relativedelta import relativedelta

scraperwiki.scrape("http://www.ballangen.kommune.no/artikler/postlister")
postlistelib=scraperwiki.swimport('postliste-python-lib')

#     <!-- $BeginBlock postjournal_liste -->
#     <tr>
#         <td class="CommonBold">&nbsp;&nbsp;&nbsp;
#             SÃ<98>KER KULTURMIDLER FOR BALLANGEN FRIIDRETT
#         </td>
#     </tr>
#     <tr>
#         <td>&nbsp;
# </td>
#     </tr>
#     <tr>
#         <td>
#             <b>Sakstittel:  </b>KULTURMIDLER 2012
# 
#         </td>
#     </tr>
#     <tr>
#         <td>&nbsp;
# </td>
#     </tr>
#     <tr>
#         <td>
#             <b>Arkivsaksnr.:  </b>12/00093 - 032 I&nbsp;&nbsp;&nbsp;&nbsp;<b>LÃ¸penr.:</b
# >002255/12
#         </td>
#     </tr>
#     <tr>
#         <td><b>Fra/Til: </b>Eirin SÃ¸rslett
# </td>
#     </tr>
#     <tr>
#         <td><b>Saksbehandler:  </b>
#         OddbjÃ¸rn DalsbÃ¸
#  (RÃ<85>D/KVO)
#         </td>
#     </tr>
#     <tr>
#         <td><b>Datert:  </b> 02.04.2012</td>
#     </tr>
#     <tr>
#         <td style="padding-bottom: 15px;">
#             &nbsp;<img src="/icons/vwsent.gif" border="0" align="top" alt="Ikon" />
#             <a href="mailto:post@ballangen.kommune.no?subject=Bestill postjournal med Ark
# ivsaksnr 12/00093 - 032 I og lÃ¸penr 002255/12">Bestill journal</a>
#         </td>
#     </tr>

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

def fetch_postjournal_day(parser, url, html, saver):
    root = lxml.html.fromstring(html)

    listdate = dateutil.parser.parse(root.cssselect("h2")[0].text_content().replace("Postlister for ",""), dayfirst=True)
    print listdate.date()
    
    entries = []
    for tr in root.cssselect("table.ui-corner-all tr"):
        tds = tr.cssselect("td")
        line = tds[0].text_content()
        entries.append(line)

# 9 or 12 lines per entry
    queue = deque(entries)
    datastore = []
    while queue:
        docdesc = (queue.popleft() + queue.popleft()).strip()
    
        casedesc = (queue.popleft() +  queue.popleft()).replace("Sakstittel:", "").strip()
    
        ref = queue.popleft().strip()
        arkivsaksref = re.sub(r"L.penr.:.+$", "", ref).replace("Arkivsaksnr.:","").strip()

        caseyear = 0
        caseseqnr = 0
        casedocseq = 0
        doctype = '?'
        caseid = 'unknown'
        matchObj = re.match( r'(\d+)/(\d+)\s*-\s*(\d+) (.+)$', arkivsaksref, re.M|re.I)
        if matchObj:
            caseyear = matchObj.group(1)
            caseseqnr = matchObj.group(2)
            casedocseq = matchObj.group(3)
            doctype = matchObj.group(4)
            caseyear = expand_year(caseyear)
            caseid = str(caseyear) + "/" + str(caseseqnr)
        else:
            print "error: invalid Arkivsaksnr: " + arkivsaksref
            matchObj = re.match( r'(\d+)/(\d+)\s*-', arkivsaksref, re.M|re.I)
            if matchObj:
                caseyear = expand_year(matchObj.group(1))
                caseseqnr = matchObj.group(2)
                caseid = str(caseyear) + "/" + str(caseseqnr)

        laapenr = re.sub(r"^.+L.penr.:", "", ref)
        journalseqnr = 0
        journalyear = 0
        journalid = 'unknown'
        if -1 != laapenr.find('/') and "/" != laapenr: # Avoid broken/empty values
            journalseqnr, journalyear = laapenr.split("/")
            journalyear = expand_year(journalyear)
            journalid = str(journalyear) + "/" + str(journalseqnr)
        else:
            print u"error: invalid Løpenr: " + laapenr

        if not parser.is_valid_doctype(doctype):
            doctype = {
                'S'   : 'N',
                'PLN' : 'N',
                'Z'   : 'N',
            }[doctype]

        fratil = queue.popleft().replace("Fra/Til:", "").strip()
        if parser.is_sender_doctype(doctype):
            fratilfield = 'sender'
        elif parser.is_recipient_doctype(doctype):
             fratilfield = 'recipient'

        saksbehandler = queue.popleft().replace("Saksbehandler:","").strip()
        saksansvarlig, bar = saksbehandler.split(" (")
        saksansvarligenhet, foo = bar.split(")")
        #print saksansvarligenhet

        recorddate = dateutil.parser.parse(queue.popleft().replace("Datert:","").strip(), dayfirst=True)

        requesturl = queue.popleft().strip()

        exemption = ""
        if -1 != requesturl.find("Gradering"):
            exemption = requesturl.replace("Gradering:", "").strip()
            requesturl = queue.popleft()
            fratil = ""

        data = {
            'agency' : parser.agency,
            'recorddate' : recorddate.date(),
            'docdesc' : docdesc,
            'casedesc' : casedesc,

            'caseyear' : int(caseyear),
            'caseseqnr' : int(caseseqnr),
            'casedocseq' : int(casedocseq),
            'caseid' : caseid,
            'doctype' : doctype,

            'journalseqnr' : int(journalseqnr),
            'journalyear' : int(journalyear),
            'journalid' : journalid,
            fratilfield : fratil,

            'saksbehandler' : saksbehandler,
            'saksansvarlig' : saksansvarlig.strip(),
            'saksansvarligenhet' : saksansvarligenhet.strip(),

            'arkivsaksref' : arkivsaksref,
            'laapenr' : laapenr,
            'exemption' : exemption,

            'scrapedurl' : url,
            'scrapestamputc' : datetime.datetime.now()
        }

#        print data
        parser.verify_entry(data)
        datastore.append(data)
    saver(unique_keys=['arkivsaksref'], data=datastore)

def fetch_postjournal_monthlist(baseurl, html):
    root = lxml.html.fromstring(html)
    subset = root.cssselect("div table")
    urls = subset[0].cssselect("td a")
    urllist = []
    for ahref in urls:
        href = ahref.attrib['href']
        if -1 != href.find("day="):
#            print href
            urllist.append(baseurl + href)
    return urllist

# http://www.offentlighet.no/

agency = "Ballangen kommune"
baseurl = "http://www.ballangen.kommune.no"

monthurls = []

def addyear(monthurls, year):
    for m in [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
        monthstr = "%02d%d" % (m, year)
        url = "http://www.ballangen.kommune.no/artikler/postlister?month=" + monthstr
        monthurls.append(url)

#addyear(monthurls, 2003)
#addyear(monthurls, 2004) # Consistency problems in http://www.ballangen.kommune.no/artikler/postlister?month=012004&day=06 (bad Arkivsaksnr. and lacking    Løpenr.)

#addyear(monthurls, 2005)
#addyear(monthurls, 2006)
#addyear(monthurls, 2007)
#addyear(monthurls, 2008)
#addyear(monthurls, 2009)
#addyear(monthurls, 2010)
#addyear(monthurls, 2011)
#addyear(monthurls, 2012)

parsemonths = 2

today = datetime.date.today()
i  = 1
while i <= parsemonths:
    i = i + 1
#    parsemonths = parsemonths - 1
    monthtoparse = today + relativedelta(months=parsemonths - i)
    monthstr = monthtoparse.strftime("%m%Y")
    url = "http://www.ballangen.kommune.no/artikler/postlister?month=" + monthstr
    monthurls.append(url)

#url = "http://www.ballangen.kommune.no/artikler/postlister?month=032012&day=19"

def reload_error_entries():
    monthurls = []
    problems = scraperwiki.sqlite.select("distinct scrapedurl from swdata where caseid = 'unknown'")
    for n in problems:
        monthurls.append(n['scrapedurl'])

print "Fetching public journal!"

parser = postlistelib.JournalParser(agency=agency)

urllist = []

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

for monthurl in monthurls:
    print "Fetching month list from " + monthurl
    html = fetch_url(monthurl)
    urllist.extend(fetch_postjournal_monthlist(baseurl = baseurl, html = html))

for dayurl in urllist:
    res = scraperwiki.sqlite.select("scrapedurl from swdata where scrapedurl = '"+dayurl+"' and scrapestamputc > '2012-06-23T15:12:40' limit 1")
    if 0 < len(res):
        continue
    print "Fetching from " + dayurl
    html = fetch_url(dayurl)
#    print html
    fetch_postjournal_day(parser=parser, url=dayurl, html=html, saver=saver)

