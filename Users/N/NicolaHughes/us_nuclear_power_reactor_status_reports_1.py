# needs to be cross-referenced to http://www.nrc.gov/info-finder/reactor/bv2.html
#Will be made into email alert and run through sql viewer

import scraperwiki
import urllib2
import urlparse
import lxml.html
import datetime
import re  

mainurl = "http://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/"

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class BadDateError(Exception):  pass

def ScrapePage(durl, ddate):
    text = urllib2.urlopen(durl).read().decode("latin1")
    root = lxml.html.fromstring(text)
    title = root.cssselect("div#bodyMainInnerSub h1")[0].text
    mtitle = re.match("Power Reactor[\- ]Status Report for (\w+) (\d+), (\d\d\d\d)", title)
    assert mtitle, title
    imonth = months.index(mtitle.group(1))
    ldate = datetime.date(int(mtitle.group(3)), imonth+1, int(mtitle.group(2)))
    if ldate != ddate:
        raise BadDateError()

    tables = root.cssselect("table table")
    assert len(tables) == 4
    ldata = [ ]
    for t in tables:
        headers = [ re.sub("[()*#]", "", th.text).strip()  for th in t[0].cssselect("th") ]

        if headers == ['Unit', 'Power', 'Down', 'Reason or Comment', 'Change in report', 'Number of Scrams']:
            pass
        elif headers == ['Unit', 'Power']:
            pass
        else:
            assert False, headers

        for row in t[1:]:
            drow = [ (d.text or "").lower().strip()  for d in row.cssselect("td") ] 
            data = dict(zip(headers, drow))
            #print data, headers
            if re.search("\.", data["Power"]):
                data["Power"] = float(data["Power"])
            else:
                data["Power"] = int(data["Power"])
            for k in ['Change in report', 'Reason or Comment', 'Down', 'Number of Scrams']:
                if k in data and not data[k]:  # 19990314ps.html has a missing cell
                    del data[k]
            assert data.get('Change in report') in [None, '*'], data
            if data.get('Number of Scrams'):
                data['Number of Scrams'] = int(data['Number of Scrams'])
            if data.get('Down'):
                mdown = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", data.get('Down'))
                assert mdown, data
                data['Down'] = datetime.date(int(mdown.group(3)), int(mdown.group(1)), int(mdown.group(2)))
            #print lxml.html.tostring(t)
            data["date"] = sdate
            ldata.append(data)
    scraperwiki.sqlite.save(["date", "Unit"], ldata)


# do we go earlier?  do we look at today?
#sdate = scraperwiki.sqlite.save_var("datelow", "1999-01-01")
while True:
    sdate = scraperwiki.sqlite.get_var("datelow", "1999-01-01")
    #print sdate
    msdate = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", sdate)
    ddate = datetime.date(int(msdate.group(1)), int(msdate.group(2)), int(msdate.group(3)))
    durl = "http://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/%04d/%04d%02d%02dps.html" % \
            (ddate.year, ddate.year, ddate.month, ddate.day)
    try:
        ScrapePage(durl, ddate)
    except urllib2.HTTPError, e:
        assert e.code == 404
        break   # needs to look at the day
        scraperwiki.sqlite.save(["date"], {"date":ddate, "durl":durl}, table_name="missing_day")
    except BadDateError:
        scraperwiki.sqlite.save(["date"], {"date":ddate, "durl":durl}, table_name="missing_day")

    nddate = ddate + datetime.timedelta(1)
    nsdate = "%04d-%02d-%02d" % (nddate.year, nddate.month, nddate.day)
    scraperwiki.sqlite.save_var("datelow", nsdate)



