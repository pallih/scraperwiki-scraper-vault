"""
Department for Energy and Climate Change: Oil & Gas: Well data


Source:
  https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell

It's a part of the long list of stuff here:
  https://www.og.decc.gov.uk/information/info_strategy/index.htm


"Oil's well that ends well"
 - The Three Stooges
"""

# Comments from JGT
# Probably less unnecessary key mangling
# use urlparse.urljoin
# why do we get httplib.IncompleteRead on some of them?
# more categorization of the wells (Abandoned, still running, depth)
# convert all depths into metres


from scraperwiki import sqlite
import urllib2
import re
import datetime
import httplib
import time

def main():
    for q in list_quadrants():
        for url in list_well_urls(q):
            scrape_well(url)


def list_quadrants():
    print "Getting Page"
    pagetext = urllib2.urlopen("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")
    print "Got Page" # Script does not get this far ...
    quadrants = []
    r = re.compile("^<OPTION>([0-9]*)$")
    for l in pagetext:
        m = r.match(l)
        if m:
            quadrants.append(int(m.groups()[0]))
    quadrants.reverse()
    return quadrants


def GetLines(url):
    lines = None
    for i in range(3):
        pagetext = urllib2.urlopen(url)
        try:
            lines = pagetext.readlines()
        except (httplib.IncompleteRead), err:
            time.sleep(1)
        if lines:
            return lines
    print "Failed", url
    return []
        


def list_well_urls(q):
    print "Making well list from quadrant %d"%q
    url = quadrant_url(q)
    lines = GetLines(url)
    r = re.compile('^<A HREF="(.*)">.*</A>$')
    base = "https://www.og.decc.gov.uk"
    urls = []
    for l in lines:
        m = r.match(l)
        if m:
            href = m.groups()[0]
            if href[:33] == "/pls/wons/wdep0100.wellHeaderData":
                urls.append(base+href)
    return urls


def quadrant_url(q):
    "Hacks up the URL format that querying the site by hand produces"
    
    base = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell?"
    early = ["f_quadNoList=***","f_quadNoList=%d"%q,"f_blockNoList=**"]
    late = ["f_blockNoList=%d"%i for i in range(1,30)]
    return base + "&".join(early+late)


def scrape_well(url):
    d = raw_well_data(url)
    d = tidy_data(d)
    ll = lat_long(d)
    print "scraped well %s"%(d["Well Registration No."])
    sqlite.save(unique_keys=["Well Registration No."],data=d,latlng=ll)


def raw_well_data(url):
    pagetext = urllib2.urlopen(url)
    it = iter(pagetext)
    r = re.compile('^<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*)</A>$')
    s = re.compile('^ = (.*)$')
    d = {}
    for l in it:
        m = r.match(l)
        if m:
            key = m.groups()[0]
            l = it.next()
            n = s.match(l)
            if n:
                value = n.groups()[0]
                d[key] = value
    return d


def tidy_data(d):
    "Does some postprocessing"
    result = dict(tidy_key_val(k,v) for (k,v) in d.iteritems())
    if result["Completion Status"] == "Abandoned":
        result["colour"] = "ff0000"
    else:
        result["colour"] = "00ff00"
    return result


def tidy_key_val(k,v):

    # capitalise
    k = " ".join(s.capitalize() for s in k.split(" "))

    # correct systematic typo
    k = k.replace("Longtitude","Longitude")

    # empty the null values
    if v=="NULL Value":
        v=""

    # make proper date objects
    elif v and "Date" in k.split(" "):
        v = make_date(v)

    return (k,v)


def make_date(s):
    (rd,rm,ry) = s.split("-")
    y = int(ry)
    m = 1 + ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"].index(rm)
    d = int(rd)
    return datetime.date(y,m,d)


def lat_long(d):
    thlat = d.get("Top Hole Latitude", "")
    thlng = d.get("Top Hole Longitude", "")
    if not thlat or not thlng:
        return None
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", thlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", thlng)
    if not mlat or not mlng:
        return None
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng
    return [lat,lng]


main()"""
Department for Energy and Climate Change: Oil & Gas: Well data


Source:
  https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell

It's a part of the long list of stuff here:
  https://www.og.decc.gov.uk/information/info_strategy/index.htm


"Oil's well that ends well"
 - The Three Stooges
"""

# Comments from JGT
# Probably less unnecessary key mangling
# use urlparse.urljoin
# why do we get httplib.IncompleteRead on some of them?
# more categorization of the wells (Abandoned, still running, depth)
# convert all depths into metres


from scraperwiki import sqlite
import urllib2
import re
import datetime
import httplib
import time

def main():
    for q in list_quadrants():
        for url in list_well_urls(q):
            scrape_well(url)


def list_quadrants():
    print "Getting Page"
    pagetext = urllib2.urlopen("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")
    print "Got Page" # Script does not get this far ...
    quadrants = []
    r = re.compile("^<OPTION>([0-9]*)$")
    for l in pagetext:
        m = r.match(l)
        if m:
            quadrants.append(int(m.groups()[0]))
    quadrants.reverse()
    return quadrants


def GetLines(url):
    lines = None
    for i in range(3):
        pagetext = urllib2.urlopen(url)
        try:
            lines = pagetext.readlines()
        except (httplib.IncompleteRead), err:
            time.sleep(1)
        if lines:
            return lines
    print "Failed", url
    return []
        


def list_well_urls(q):
    print "Making well list from quadrant %d"%q
    url = quadrant_url(q)
    lines = GetLines(url)
    r = re.compile('^<A HREF="(.*)">.*</A>$')
    base = "https://www.og.decc.gov.uk"
    urls = []
    for l in lines:
        m = r.match(l)
        if m:
            href = m.groups()[0]
            if href[:33] == "/pls/wons/wdep0100.wellHeaderData":
                urls.append(base+href)
    return urls


def quadrant_url(q):
    "Hacks up the URL format that querying the site by hand produces"
    
    base = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell?"
    early = ["f_quadNoList=***","f_quadNoList=%d"%q,"f_blockNoList=**"]
    late = ["f_blockNoList=%d"%i for i in range(1,30)]
    return base + "&".join(early+late)


def scrape_well(url):
    d = raw_well_data(url)
    d = tidy_data(d)
    ll = lat_long(d)
    print "scraped well %s"%(d["Well Registration No."])
    sqlite.save(unique_keys=["Well Registration No."],data=d,latlng=ll)


def raw_well_data(url):
    pagetext = urllib2.urlopen(url)
    it = iter(pagetext)
    r = re.compile('^<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*)</A>$')
    s = re.compile('^ = (.*)$')
    d = {}
    for l in it:
        m = r.match(l)
        if m:
            key = m.groups()[0]
            l = it.next()
            n = s.match(l)
            if n:
                value = n.groups()[0]
                d[key] = value
    return d


def tidy_data(d):
    "Does some postprocessing"
    result = dict(tidy_key_val(k,v) for (k,v) in d.iteritems())
    if result["Completion Status"] == "Abandoned":
        result["colour"] = "ff0000"
    else:
        result["colour"] = "00ff00"
    return result


def tidy_key_val(k,v):

    # capitalise
    k = " ".join(s.capitalize() for s in k.split(" "))

    # correct systematic typo
    k = k.replace("Longtitude","Longitude")

    # empty the null values
    if v=="NULL Value":
        v=""

    # make proper date objects
    elif v and "Date" in k.split(" "):
        v = make_date(v)

    return (k,v)


def make_date(s):
    (rd,rm,ry) = s.split("-")
    y = int(ry)
    m = 1 + ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"].index(rm)
    d = int(rd)
    return datetime.date(y,m,d)


def lat_long(d):
    thlat = d.get("Top Hole Latitude", "")
    thlng = d.get("Top Hole Longitude", "")
    if not thlat or not thlng:
        return None
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", thlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", thlng)
    if not mlat or not mlng:
        return None
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng
    return [lat,lng]


main()