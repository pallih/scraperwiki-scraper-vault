import scraperwiki
import lxml.etree
import lxml.html
#import re
from httplib import BadStatusLine

scraperwiki.sqlite.attach("createpsflinks")
data = scraperwiki.sqlite.select("* from createpsflinks.BasicUrl order by SID")
#alphreg=re.compile("(\D+$)")

def getbasicUrl(sid):
    urlist = []
    urlist.append("http://www.fsa.gov.uk/register/psdFirmDiscHistory.do?sid=")
    sidstring=str(sid)
    urlist.append(sidstring)
    url="".join(urlist)
    return url
    
def grabTitle (root):
    title = root.cssselect ("p.strong")
    regvar = title[0].text_content()
    return regvar

def grabLinks(sid):
    url = getbasicUrl(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = grabTitle(root)
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID":sid, "CompanyName":title},table_name='Companies')
    rows = root.cssselect("table.search-results tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['SID'] = sid
            record['Date'] = table_cells[0].text
            record['Action'] = table_cells[1].text_content()
            scraperwiki.sqlite.save([], record, table_name='Discipline')
try:
    scraperwiki.sqlite.execute("create table Discipline(SID string, Date string, Action string)")
    scraperwiki.sqlite.execute("create table Companies(SID string, CompanyName string)")
    scraperwiki.sqlite.execute("create table Error(SID string)")
except:
    print "Table probably already exists."
for d in data:
    try:
        grabLinks(d["SID"] )
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"]}, table_name='Error')

import scraperwiki
import lxml.etree
import lxml.html
#import re
from httplib import BadStatusLine

scraperwiki.sqlite.attach("createpsflinks")
data = scraperwiki.sqlite.select("* from createpsflinks.BasicUrl order by SID")
#alphreg=re.compile("(\D+$)")

def getbasicUrl(sid):
    urlist = []
    urlist.append("http://www.fsa.gov.uk/register/psdFirmDiscHistory.do?sid=")
    sidstring=str(sid)
    urlist.append(sidstring)
    url="".join(urlist)
    return url
    
def grabTitle (root):
    title = root.cssselect ("p.strong")
    regvar = title[0].text_content()
    return regvar

def grabLinks(sid):
    url = getbasicUrl(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = grabTitle(root)
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID":sid, "CompanyName":title},table_name='Companies')
    rows = root.cssselect("table.search-results tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['SID'] = sid
            record['Date'] = table_cells[0].text
            record['Action'] = table_cells[1].text_content()
            scraperwiki.sqlite.save([], record, table_name='Discipline')
try:
    scraperwiki.sqlite.execute("create table Discipline(SID string, Date string, Action string)")
    scraperwiki.sqlite.execute("create table Companies(SID string, CompanyName string)")
    scraperwiki.sqlite.execute("create table Error(SID string)")
except:
    print "Table probably already exists."
for d in data:
    try:
        grabLinks(d["SID"] )
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"]}, table_name='Error')

