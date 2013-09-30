import scraperwiki
import urllib2
import lxml.html
import datetime
import time
import dateutil.parser
import pickle 
import re

from datetime import date
from datetime import timedelta
from time import strftime

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.ssb.no/omssb/journal/")

postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = "Statistisk sentralbyrå"

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)

def expand_year(year):
    year = int(year)
    if year > 50:
        year = year + 1900
    else:
        year = year + 2000
    return year

def fetch_url(url):
    html = None
    for n in [1]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html
    
def save_date(parser, date, url, html):
    num_saved = 0
    root = lxml.html.fromstring(html)    
    journal_date = dateutil.parser.parse(root.cssselect("p")[0].text_content().replace("Journaldato: ",""), dayfirst=True)
    if date == journal_date.date():
        datastore = []
        for table in root.cssselect("table"):
            docid = table.cssselect("tr")[0].cssselect("p")[1].text.strip()
            datedesc = table.cssselect("tr")[0].cssselect("td")[3].cssselect("p")[0].text.strip()

            exemption = table.cssselect("tr")[1].cssselect("td")[5].cssselect("p")[0].text.strip()

            fratil_indicator = table.cssselect("tr")[2].cssselect("td")[0].cssselect("p")[0].text.strip()

            doctype = ""
            if fratil_indicator.startswith("Til"):
                doctype = "U"
            elif fratil_indicator.startswith("Fra"):
                doctype = "I"
            elif fratil_indicator.startswith("Notat fra"):
                doctype = "N"
            else: 
                raise ValueError("Fant ikke doctype %s" % fratil_indicator)

            fratil_agency = table.cssselect("tr")[2].cssselect("td")[1].cssselect("p")[0].text.strip()
 
            casedesc = table.cssselect("tr")[4].cssselect("td")[1].cssselect("p")[0].text.strip()

            docdesc = table.cssselect("tr")[5].cssselect("td")[1].cssselect("p")[0].text.strip()
            saksb = table.cssselect("tr")[0].cssselect("p")[5].text.strip()

            docdate = dateutil.parser.parse(datedesc.strip(), dayfirst=True)

            matchObj = re.match( r'(\d+)/(\d+)\s*-\s*(\d+)$', docid, re.M|re.I)
            if matchObj:
                caseyear = matchObj.group(1)
                caseseqnr = matchObj.group(2)
                casedocseq = matchObj.group(3)
                caseyear = expand_year(caseyear)
                caseid = str(caseyear) + "/" + str(caseseqnr)
            else:
                print "error: invalid Arkivsaksnr: " + docid
                matchObj = re.match( r'(\d+)/(\d+)\s*-', docid, re.M|re.I)
                if matchObj:
                    caseyear = expand_year(matchObj.group(1))
                    caseseqnr = matchObj.group(2)
                    caseid = str(caseyear) + "/" + str(caseseqnr)
            
            if parser.is_sender_doctype(doctype):
                fratilfield = 'sender'
            elif parser.is_recipient_doctype(doctype):
                 fratilfield = 'recipient'

            data = {
                'agency' : agency,
                'docdate' : docdate.date(),
                'recorddate' : journal_date.date(),
                'docdesc' : docdesc,
                'casedesc' : casedesc,
                'caseid' : caseid,
                'docid' : docid,

                'caseyear' : caseyear,
                'caseseqnr' : caseseqnr,
                'casedocseq' : casedocseq,
                
                fratilfield : fratil_agency,
                'doctype' : doctype,

                'saksbehandler' : saksb,

                'exemption' : exemption,
                
                'scrapedurl' : url,
                'scrapestamputc' : datetime.datetime.now()
                }
            parser.verify_entry(data)
            datastore.append(data)
        scraperwiki.sqlite.save(unique_keys=['docid'], data=datastore)
        num_saved += len(datastore)
        datastore = []
        #print "Saved %s" % data['caseid']
    else:
        # TODO: log error or exit?
        msg = "Tried to scrape %s but got %s" % (date, journal_date.date())
        #raise ValueError(msg)
        print msg

    return num_saved

def scrape_date(parser, date):
    url = base_url % (strftime("%d%m%y", date.timetuple()))
    html = fetch_url(url)
    if html:
        return save_date(parser, date, url, html)

base_url = 'http://www.ssb.no/omssb/journal/OJ%s.htm'
end_date = date.today()

#print res

start_date_obj = scraperwiki.sqlite.get_var('last_finished_date')

if start_date_obj:
    start_date = pickle.loads(start_date_obj)
else:
    start_date = datetime.date(2011, 1, 3)

print "Start date %s" % start_date

parser = postlistelib.JournalParser(agency=agency)

for single_date in daterange(start_date, end_date):
    if single_date.weekday() < 5:
        num_saved = scrape_date(parser, single_date)
        print "Scraped %s found %s" % (single_date, num_saved)
        if num_saved > 0:
            scraperwiki.sqlite.save_var('last_finished_date', pickle.dumps(single_date)) 

        if num_saved == None: 
            print "No more new. Exit..."
            break
import scraperwiki
import urllib2
import lxml.html
import datetime
import time
import dateutil.parser
import pickle 
import re

from datetime import date
from datetime import timedelta
from time import strftime

# Make sure Scraperwiki believe this is the source from this database
scraperwiki.scrape("http://www.ssb.no/omssb/journal/")

postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = "Statistisk sentralbyrå"

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)

def expand_year(year):
    year = int(year)
    if year > 50:
        year = year + 1900
    else:
        year = year + 2000
    return year

def fetch_url(url):
    html = None
    for n in [1]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html
    
def save_date(parser, date, url, html):
    num_saved = 0
    root = lxml.html.fromstring(html)    
    journal_date = dateutil.parser.parse(root.cssselect("p")[0].text_content().replace("Journaldato: ",""), dayfirst=True)
    if date == journal_date.date():
        datastore = []
        for table in root.cssselect("table"):
            docid = table.cssselect("tr")[0].cssselect("p")[1].text.strip()
            datedesc = table.cssselect("tr")[0].cssselect("td")[3].cssselect("p")[0].text.strip()

            exemption = table.cssselect("tr")[1].cssselect("td")[5].cssselect("p")[0].text.strip()

            fratil_indicator = table.cssselect("tr")[2].cssselect("td")[0].cssselect("p")[0].text.strip()

            doctype = ""
            if fratil_indicator.startswith("Til"):
                doctype = "U"
            elif fratil_indicator.startswith("Fra"):
                doctype = "I"
            elif fratil_indicator.startswith("Notat fra"):
                doctype = "N"
            else: 
                raise ValueError("Fant ikke doctype %s" % fratil_indicator)

            fratil_agency = table.cssselect("tr")[2].cssselect("td")[1].cssselect("p")[0].text.strip()
 
            casedesc = table.cssselect("tr")[4].cssselect("td")[1].cssselect("p")[0].text.strip()

            docdesc = table.cssselect("tr")[5].cssselect("td")[1].cssselect("p")[0].text.strip()
            saksb = table.cssselect("tr")[0].cssselect("p")[5].text.strip()

            docdate = dateutil.parser.parse(datedesc.strip(), dayfirst=True)

            matchObj = re.match( r'(\d+)/(\d+)\s*-\s*(\d+)$', docid, re.M|re.I)
            if matchObj:
                caseyear = matchObj.group(1)
                caseseqnr = matchObj.group(2)
                casedocseq = matchObj.group(3)
                caseyear = expand_year(caseyear)
                caseid = str(caseyear) + "/" + str(caseseqnr)
            else:
                print "error: invalid Arkivsaksnr: " + docid
                matchObj = re.match( r'(\d+)/(\d+)\s*-', docid, re.M|re.I)
                if matchObj:
                    caseyear = expand_year(matchObj.group(1))
                    caseseqnr = matchObj.group(2)
                    caseid = str(caseyear) + "/" + str(caseseqnr)
            
            if parser.is_sender_doctype(doctype):
                fratilfield = 'sender'
            elif parser.is_recipient_doctype(doctype):
                 fratilfield = 'recipient'

            data = {
                'agency' : agency,
                'docdate' : docdate.date(),
                'recorddate' : journal_date.date(),
                'docdesc' : docdesc,
                'casedesc' : casedesc,
                'caseid' : caseid,
                'docid' : docid,

                'caseyear' : caseyear,
                'caseseqnr' : caseseqnr,
                'casedocseq' : casedocseq,
                
                fratilfield : fratil_agency,
                'doctype' : doctype,

                'saksbehandler' : saksb,

                'exemption' : exemption,
                
                'scrapedurl' : url,
                'scrapestamputc' : datetime.datetime.now()
                }
            parser.verify_entry(data)
            datastore.append(data)
        scraperwiki.sqlite.save(unique_keys=['docid'], data=datastore)
        num_saved += len(datastore)
        datastore = []
        #print "Saved %s" % data['caseid']
    else:
        # TODO: log error or exit?
        msg = "Tried to scrape %s but got %s" % (date, journal_date.date())
        #raise ValueError(msg)
        print msg

    return num_saved

def scrape_date(parser, date):
    url = base_url % (strftime("%d%m%y", date.timetuple()))
    html = fetch_url(url)
    if html:
        return save_date(parser, date, url, html)

base_url = 'http://www.ssb.no/omssb/journal/OJ%s.htm'
end_date = date.today()

#print res

start_date_obj = scraperwiki.sqlite.get_var('last_finished_date')

if start_date_obj:
    start_date = pickle.loads(start_date_obj)
else:
    start_date = datetime.date(2011, 1, 3)

print "Start date %s" % start_date

parser = postlistelib.JournalParser(agency=agency)

for single_date in daterange(start_date, end_date):
    if single_date.weekday() < 5:
        num_saved = scrape_date(parser, single_date)
        print "Scraped %s found %s" % (single_date, num_saved)
        if num_saved > 0:
            scraperwiki.sqlite.save_var('last_finished_date', pickle.dumps(single_date)) 

        if num_saved == None: 
            print "No more new. Exit..."
            break
