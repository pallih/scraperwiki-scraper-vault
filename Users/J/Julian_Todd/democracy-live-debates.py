import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


import scraperwiki
import urllib
import re
import datetime

import lxml.html
import lxml.etree


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def Main():
    # iterate through the days in the past to get the full lookup
    #dlast = datetime.date(2010, 6, 6)  # broken link on 2010-03-01
    dlast = datetime.date.today()
    for i in range(5, 15):
        d = dlast - datetime.timedelta(i)
        daydebates = ParseSchedule(d)
        print "scraping:", i, d, len(daydebates)
        for data in daydebates:
            data["description"], data["lastupdateddate"] = GetDescription(data["link"])
        scraperwiki.sqlite.save(unique_keys=["link"], data=daydebates)



def GetDescription(link):
    doc = lxml.html.parse(link)
    root = doc.getroot()
    #print lxml.etree.tostring(root)

    #Page last updated at 08:59 GMT, Tuesday, 21 September 2010 09:59 UK
    lastupdated = root.cssselect("div.ds")[0]
    sblastupdated = lxml.etree.tostring(lastupdated)
    rlu = 'Page last updated at </span>(\d\d):(\d\d) GMT, \w+, (\d+) (\w+) (\d\d\d\d)(?: (\d\d):(\d\d) UK)?</div>'
    mlu = re.search(rlu, sblastupdated)
    if not mlu:
        print "??", sblastupdated
        lastupdateddate = None
    else:
        assert mlu.group(4) in months, mlu.groups()
        month = months.index(mlu.group(4)) + 1
        lastupdateddate = datetime.datetime(int(mlu.group(5)), month, int(mlu.group(3)), int(mlu.group(1)), int(mlu.group(2)))
#        print lastupdateddate, sblastupdated
        
    storybody = root.cssselect("div.storybody")[0]
    sbtext = lxml.etree.tostring(storybody)
    sbtext = re.sub("<p>", "--NEWLINE--", sbtext)
    sbtext = re.sub("<[^>]*>", "", sbtext)
    sbtext = re.sub("&#13;", " ", sbtext)
    sbtext = re.sub("&#163;", "£", sbtext)
    sbtext = re.sub("&#8226;", "*", sbtext)  # bullet point
    sbtext = re.sub("\s+", " ", sbtext)
    sbtext = sbtext.strip()
    sbtext = re.sub("\s*--NEWLINE--\s*", "\n\n", sbtext)
    return sbtext, lastupdateddate
    


def ParseSchedule(date):
    urlschedule = "http://news.bbc.co.uk/democracylive/hi/schedule/date/%s" % str(date)
    doc = lxml.html.parse(urlschedule)
    root = doc.getroot()
    h4alist = root.cssselect("h4 a")
    daydebates = [ ]
    for h4a in h4alist:
        #print lxml.etree.tostring(h4a)
        link = h4a.get("href")
        title = h4a.find("span").tail
        body = re.match("http://news.bbc.co.uk/democracylive/hi/(\w+)/", link).group(1)
        data = { "body":body, "link":link, "title":title, "date":date }
        daydebates.append(data)
    return daydebates


Main()


