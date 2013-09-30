import scraperwiki
import lxml.etree
import lxml.html
import re
from httplib import BadStatusLine

scraperwiki.sqlite.attach("testscraper_6")
data = scraperwiki.sqlite.select("* from testscraper_6.Firms order by SID")
alphreg=re.compile("[\w]+")

def regFind(str):    
    m=alphreg.search(str)
    if m is not None:
        return True
    else:
        return False

def getbasicUrl(sid):
    urlist = []
    urlist.append("http://www.fsa.gov.uk/register/firmContact.do?sid=")
    sidstring=str(sid)
    urlist.append(sidstring)
    url="".join(urlist)
    return url
 
def grabfirstLine (root):
    row = root.cssselect ("table.basic-information1 tr")[1]
    data = row.cssselect("td")[0]
    name = data.text
    return name
   
def grabName (root):
    row = root.cssselect ("table.basic-information1 tr")[0]
    data = row.cssselect("td")[0]
    if regFind(data.text) is True:
        name = data.text
        return name
    else:
        return grabfirstLine(root)

def grabLinks(sid):
    url = getbasicUrl(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = grabName(root)
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID":sid, "ContactName":title},table_name='Contact')

try:
    scraperwiki.sqlite.execute("create table Contact(SID string, ContactName string)")
    scraperwiki.sqlite.execute("create table Error(SID string)")
except:
    print "Table probably already exists."
for d in data:
    try:
        grabLinks(d["SID"] )
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"]})


import scraperwiki
import lxml.etree
import lxml.html
import re
from httplib import BadStatusLine

scraperwiki.sqlite.attach("testscraper_6")
data = scraperwiki.sqlite.select("* from testscraper_6.Firms order by SID")
alphreg=re.compile("[\w]+")

def regFind(str):    
    m=alphreg.search(str)
    if m is not None:
        return True
    else:
        return False

def getbasicUrl(sid):
    urlist = []
    urlist.append("http://www.fsa.gov.uk/register/firmContact.do?sid=")
    sidstring=str(sid)
    urlist.append(sidstring)
    url="".join(urlist)
    return url
 
def grabfirstLine (root):
    row = root.cssselect ("table.basic-information1 tr")[1]
    data = row.cssselect("td")[0]
    name = data.text
    return name
   
def grabName (root):
    row = root.cssselect ("table.basic-information1 tr")[0]
    data = row.cssselect("td")[0]
    if regFind(data.text) is True:
        name = data.text
        return name
    else:
        return grabfirstLine(root)

def grabLinks(sid):
    url = getbasicUrl(sid)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    title = grabName(root)
    scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID":sid, "ContactName":title},table_name='Contact')

try:
    scraperwiki.sqlite.execute("create table Contact(SID string, ContactName string)")
    scraperwiki.sqlite.execute("create table Error(SID string)")
except:
    print "Table probably already exists."
for d in data:
    try:
        grabLinks(d["SID"] )
    except BadStatusLine:
        scraperwiki.sqlite.save(unique_keys=["SID"], data={"SID": d["SID"]})


