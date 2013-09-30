# -*- coding: utf8 -*- 
import scraperwiki
import urllib
from BeautifulSoup import BeautifulSoup
import datetime

def datestr2date(datestr):
# "22. oktober 2009"
    months = {
        'januar'    : 1,
        'februar'   : 2,
        'mars'      : 3,
        'april'     : 4,
        'mai'       : 5,
        'juni'      : 6,
        'juli'      : 7,
        'august'    : 8,
        'september' : 9,
        'oktober'   :10,
        'november'  :11,
        'desember'  :12,
    }
    day, month, year = datestr.split(" ")
    day = int(day.split(".")[0])
    month = months[month]
    year = int(year)
    return datetime.date(year, month, day)
def scrapepdf(pdfurl):
    print "scraping " + pdfurl
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    s = BeautifulSoup(pdfxml)
    print s

    casenr = None
    datestr = None
    daynr = None
    last_line = ""
    for text in s.findAll('text'):
        msg = text.text
        #print msg
        if 0 == msg.find(u"Møte "):
            datestr = datestr2date(msg.split("den ")[1].split(" kl.")[0])
            #print datestr
        if 0 == msg.find("D a g s o r d e n (nr."):
            daynr = msg.split(")")[0].split(".")[1]
            continue
        if -1 != msg.find("Votering i sak nr."):
            print msg
            casenr = msg.split("nr.")[1].strip()
            continue
        elif -1 != msg.find("Votering i sak "):
            print msg
            casenr = msg.split("i sak ")[1].strip()
            continue
        if -1 != msg.find("enstemmig bifalt") or -1 != msg.find("enstemmig vedtatt") or ((-1 != msg.find("bifalt") or -1 != msg.find("vedtatt")) and -1 != last_line.find("enstemmig")):         
            print datestr, daynr, casenr, msg
            data = {
                'date' : datestr,
                'daynr' : daynr,
                'casenum' : casenr,
                'msg' : last_line + msg,
            }
            if casenr is not None:
                scraperwiki.sqlite.save(unique_keys=['date', 'casenum'], data=data)
        last_line = msg
        

# <text top="130" left="126" width="264" height="13" font="0"><b>Møte torsdag den 22. oktober 2009 kl. 10</b></text>
# <text top="209" left="118" width="140" height="13" font="1">D a g s o r d e n (nr. 7):</text>
# <text top="708" left="478" width="261" height="13" font="1">Komiteens innstilling ble enstemmig bifalt.</text>
# <text top="130" left="584" width="115" height="13" font="2"><i>Votering i sak nr. 9</i></text>


def test():
    urls = [
#        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091001.pdf",
#        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091022.pdf",
        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091211.pdf",
    ]
    for pdfurl in urls:
        scrapepdf(pdfurl)

#test()
#exit(0)

baseurl = "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/"
for yearmonth in ('0910', '0911', '0912', '1001', '1002', '1003', '1004', '1005', '1006'):
    for day in xrange(31):
        pdfurl = baseurl + "s%s%02d.pdf" % (yearmonth, day)
        scrapepdf(pdfurl)# -*- coding: utf8 -*- 
import scraperwiki
import urllib
from BeautifulSoup import BeautifulSoup
import datetime

def datestr2date(datestr):
# "22. oktober 2009"
    months = {
        'januar'    : 1,
        'februar'   : 2,
        'mars'      : 3,
        'april'     : 4,
        'mai'       : 5,
        'juni'      : 6,
        'juli'      : 7,
        'august'    : 8,
        'september' : 9,
        'oktober'   :10,
        'november'  :11,
        'desember'  :12,
    }
    day, month, year = datestr.split(" ")
    day = int(day.split(".")[0])
    month = months[month]
    year = int(year)
    return datetime.date(year, month, day)
def scrapepdf(pdfurl):
    print "scraping " + pdfurl
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    s = BeautifulSoup(pdfxml)
    print s

    casenr = None
    datestr = None
    daynr = None
    last_line = ""
    for text in s.findAll('text'):
        msg = text.text
        #print msg
        if 0 == msg.find(u"Møte "):
            datestr = datestr2date(msg.split("den ")[1].split(" kl.")[0])
            #print datestr
        if 0 == msg.find("D a g s o r d e n (nr."):
            daynr = msg.split(")")[0].split(".")[1]
            continue
        if -1 != msg.find("Votering i sak nr."):
            print msg
            casenr = msg.split("nr.")[1].strip()
            continue
        elif -1 != msg.find("Votering i sak "):
            print msg
            casenr = msg.split("i sak ")[1].strip()
            continue
        if -1 != msg.find("enstemmig bifalt") or -1 != msg.find("enstemmig vedtatt") or ((-1 != msg.find("bifalt") or -1 != msg.find("vedtatt")) and -1 != last_line.find("enstemmig")):         
            print datestr, daynr, casenr, msg
            data = {
                'date' : datestr,
                'daynr' : daynr,
                'casenum' : casenr,
                'msg' : last_line + msg,
            }
            if casenr is not None:
                scraperwiki.sqlite.save(unique_keys=['date', 'casenum'], data=data)
        last_line = msg
        

# <text top="130" left="126" width="264" height="13" font="0"><b>Møte torsdag den 22. oktober 2009 kl. 10</b></text>
# <text top="209" left="118" width="140" height="13" font="1">D a g s o r d e n (nr. 7):</text>
# <text top="708" left="478" width="261" height="13" font="1">Komiteens innstilling ble enstemmig bifalt.</text>
# <text top="130" left="584" width="115" height="13" font="2"><i>Votering i sak nr. 9</i></text>


def test():
    urls = [
#        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091001.pdf",
#        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091022.pdf",
        "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/s091211.pdf",
    ]
    for pdfurl in urls:
        scrapepdf(pdfurl)

#test()
#exit(0)

baseurl = "http://stortinget.no/Global/pdf/Referater/Stortinget/2009-2010/"
for yearmonth in ('0910', '0911', '0912', '1001', '1002', '1003', '1004', '1005', '1006'):
    for day in xrange(31):
        pdfurl = baseurl + "s%s%02d.pdf" % (yearmonth, day)
        scrapepdf(pdfurl)