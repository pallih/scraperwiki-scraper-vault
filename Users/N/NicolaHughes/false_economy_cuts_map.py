import scraperwiki
import urllib2
import lxml.html
import re
import urlparse
import datetime


                    

url = 'http://falseeconomy.org.uk/cuts/uk/all/t1'

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def ParsePage(purl):
    data = { "url":purl }
    proot = lxml.html.parse(purl).getroot()
    h1 = proot.cssselect("#article h1")[0]

    data["title"] = h1.text[:-1]
    h1post = h1.cssselect(".h1post")
    if h1post:
        data["h1post"] = h1post[0].text

    tbs = proot.cssselect("#article .tightbox strong")
    assert tbs[0].text == "Location:"
    loclist = [ ]
    loca = tbs[0].getnext()
    while loca is not None:
        loclist.append(loca.text)
        loca = loca.getnext()
    data["location"] = " > ".join(loclist)

    assert tbs[1].text == "Sector:"
    seclist = [ ]
    seca = tbs[1].getnext()
    while seca is not None:
        seclist.append(seca.text)
        seca = seca.getnext()
    data["Sectors"] = ",".join(seclist)

    #print "xx", lxml.html.tostring(proot)

    contents = [ ]
    el = tbs[1].getparent().getnext()
    while el.tag != "ul" or el.attrib.get("class") != "moreinfo":
        contents.append(lxml.html.tostring(el))
        el = el.getnext()
    data["description"] = "\n\n".join(contents)

    moreinfo = el.cssselect("strong")
    if moreinfo[0].text == "Source:":
        data["source"] = moreinfo[0].getnext().attrib.get("href")

    assert moreinfo[-1].text == "Posted by:"
    mpb = re.match("(.*?) at (\d+):(\d+)([ap]m) on (\d+) (\w+) (\d\d\d\d)$", moreinfo[-1].tail.strip())
    data["postedby"] = mpb.group(1)
    month = months.index(mpb.group(6))+1
    hour = int(mpb.group(2))
    if mpb.group(4) == "pm" and hour != 12:
        hour += 12
    data["date"] = datetime.datetime(int(mpb.group(7)), month, int(mpb.group(5)), hour, int(mpb.group(3)))    
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)


def ParseIndex(root):
    for h3a in root.cssselect("div#idTab1 h3 a"):
        purl = urlparse.urljoin(url, h3a.attrib.get("href"))
        ParsePage(purl)


urlsvisited = [ ]
urlsleft = [ url ]

ipage = 0
while urlsleft:
    ipage += 1
    url = urlsleft.pop(0)
    root = lxml.html.parse(url).getroot()
    print "Doing index page", ipage, url
    if ipage >= 0:
        ParseIndex(root)
    else:
        print "Skipping"

    plinks = [ a.attrib.get("href")  for a in root.cssselect("a")  if re.search("cuts/uk/all/t1/P\d+", a.attrib.get("href")) ]
    urlsvisited.append(url)
    for lk in plinks:
        if lk not in urlsvisited and lk not in urlsleft:
            urlsleft.append(lk)




import scraperwiki
import urllib2
import lxml.html
import re
import urlparse
import datetime


                    

url = 'http://falseeconomy.org.uk/cuts/uk/all/t1'

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def ParsePage(purl):
    data = { "url":purl }
    proot = lxml.html.parse(purl).getroot()
    h1 = proot.cssselect("#article h1")[0]

    data["title"] = h1.text[:-1]
    h1post = h1.cssselect(".h1post")
    if h1post:
        data["h1post"] = h1post[0].text

    tbs = proot.cssselect("#article .tightbox strong")
    assert tbs[0].text == "Location:"
    loclist = [ ]
    loca = tbs[0].getnext()
    while loca is not None:
        loclist.append(loca.text)
        loca = loca.getnext()
    data["location"] = " > ".join(loclist)

    assert tbs[1].text == "Sector:"
    seclist = [ ]
    seca = tbs[1].getnext()
    while seca is not None:
        seclist.append(seca.text)
        seca = seca.getnext()
    data["Sectors"] = ",".join(seclist)

    #print "xx", lxml.html.tostring(proot)

    contents = [ ]
    el = tbs[1].getparent().getnext()
    while el.tag != "ul" or el.attrib.get("class") != "moreinfo":
        contents.append(lxml.html.tostring(el))
        el = el.getnext()
    data["description"] = "\n\n".join(contents)

    moreinfo = el.cssselect("strong")
    if moreinfo[0].text == "Source:":
        data["source"] = moreinfo[0].getnext().attrib.get("href")

    assert moreinfo[-1].text == "Posted by:"
    mpb = re.match("(.*?) at (\d+):(\d+)([ap]m) on (\d+) (\w+) (\d\d\d\d)$", moreinfo[-1].tail.strip())
    data["postedby"] = mpb.group(1)
    month = months.index(mpb.group(6))+1
    hour = int(mpb.group(2))
    if mpb.group(4) == "pm" and hour != 12:
        hour += 12
    data["date"] = datetime.datetime(int(mpb.group(7)), month, int(mpb.group(5)), hour, int(mpb.group(3)))    
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)


def ParseIndex(root):
    for h3a in root.cssselect("div#idTab1 h3 a"):
        purl = urlparse.urljoin(url, h3a.attrib.get("href"))
        ParsePage(purl)


urlsvisited = [ ]
urlsleft = [ url ]

ipage = 0
while urlsleft:
    ipage += 1
    url = urlsleft.pop(0)
    root = lxml.html.parse(url).getroot()
    print "Doing index page", ipage, url
    if ipage >= 0:
        ParseIndex(root)
    else:
        print "Skipping"

    plinks = [ a.attrib.get("href")  for a in root.cssselect("a")  if re.search("cuts/uk/all/t1/P\d+", a.attrib.get("href")) ]
    urlsvisited.append(url)
    for lk in plinks:
        if lk not in urlsvisited and lk not in urlsleft:
            urlsleft.append(lk)




