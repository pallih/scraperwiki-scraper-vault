import urllib
import urlparse
import lxml.html
import re
import scraperwiki
import datetime

seasons = [u"Fr\xfchjahr", u"Sommer", u"Herbst", u"Winter"]
def convertdate(d):
    #print "date is ", [d]
    print "date is ", [d]
    md = re.match("(?u)(\d+)\. (\w+) (\d+)$", d)
    #print "month is ", [md.group(2)]
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1)))

def part(alink):
    html = urllib.urlopen(alink).read()
    #print html
    root = lxml.html.fromstring(html)
    trs = root.cssselect("div#INHALT table tr")
    #remove table header
    trs.pop(0)
    for tr in trs:
        tds=tr.cssselect("td")
        #year
        if(re.match('^\d+',tds[0].text_content().strip())):
            year=tds[0].text_content().strip()

        orig_date=tds[1].text_content().strip()
        #date
        if(re.match('^\d+.*',tds[1].text_content().strip())):
            date=tds[1].text_content().strip().split('.')
            startdate = enddate = year + '-' + date[1] + '-' + date[0]
             
        elif(re.match('.*(Fr\xfchjahr).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-01-01"
            enddate = year + "-03-31"
        elif(re.match('.*(Sommer).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-04-01"
            enddate = year + "-06-30"
        elif(re.match('.*(Herbst).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-07-01"
            enddate = year + "-09-30"
        elif(re.match('.*(Winter).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-10-01"
            enddate = year + "-12-31"

        else:
            continue

        
        data = {"year": year, "orig_date": orig_date, "startdate":startdate, "enddate": enddate, "state": tds[2].text_content().strip(), "electiontype": tds[3].text_content().strip(), "frequency": tds[4].text_content().strip()}
        print data
        scraperwiki.sqlite.save(["year", "state","electiontype"], data)




url = "http://www.bundeswahlleiter.de/de/kuenftige_wahlen/"
part(url)


import urllib
import urlparse
import lxml.html
import re
import scraperwiki
import datetime

seasons = [u"Fr\xfchjahr", u"Sommer", u"Herbst", u"Winter"]
def convertdate(d):
    #print "date is ", [d]
    print "date is ", [d]
    md = re.match("(?u)(\d+)\. (\w+) (\d+)$", d)
    #print "month is ", [md.group(2)]
    imonth = months.index(md.group(2)) + 1
    return datetime.date(int(md.group(3)), imonth, int(md.group(1)))

def part(alink):
    html = urllib.urlopen(alink).read()
    #print html
    root = lxml.html.fromstring(html)
    trs = root.cssselect("div#INHALT table tr")
    #remove table header
    trs.pop(0)
    for tr in trs:
        tds=tr.cssselect("td")
        #year
        if(re.match('^\d+',tds[0].text_content().strip())):
            year=tds[0].text_content().strip()

        orig_date=tds[1].text_content().strip()
        #date
        if(re.match('^\d+.*',tds[1].text_content().strip())):
            date=tds[1].text_content().strip().split('.')
            startdate = enddate = year + '-' + date[1] + '-' + date[0]
             
        elif(re.match('.*(Fr\xfchjahr).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-01-01"
            enddate = year + "-03-31"
        elif(re.match('.*(Sommer).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-04-01"
            enddate = year + "-06-30"
        elif(re.match('.*(Herbst).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-07-01"
            enddate = year + "-09-30"
        elif(re.match('.*(Winter).*',tds[1].text_content(),flags=re.DOTALL)):
            startdate=year + "-10-01"
            enddate = year + "-12-31"

        else:
            continue

        
        data = {"year": year, "orig_date": orig_date, "startdate":startdate, "enddate": enddate, "state": tds[2].text_content().strip(), "electiontype": tds[3].text_content().strip(), "frequency": tds[4].text_content().strip()}
        print data
        scraperwiki.sqlite.save(["year", "state","electiontype"], data)




url = "http://www.bundeswahlleiter.de/de/kuenftige_wahlen/"
part(url)


