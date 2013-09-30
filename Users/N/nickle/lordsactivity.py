import urllib2
import re
import scraperwiki

START   = 2006
FINISH  = 2011

def GetActivity (start, finish):
    urlpat  = r"http://www.publications.parliament.uk/pa/ld20%02d%02d/ldhansrd/ldallfiles/peers/hansardbylord_atoz.htm"
    pat     = re.compile ('<a href="lord_hansard_(.*?)_home.html">(.*?), (.*?)</a>')
    activity= []
    for year in range (start, finish):
        y = year % 100
        url = urlpat % (y, y+1)
        html = scraperwiki.scrape (url)
        for m in pat.finditer (html):
            code = m.group (1)
            name = m.group (3) + " " + m.group(2)
            activity.append ((code, name, year))
    return activity

def Main():
    activity= GetActivity (START, FINISH)
    print len(activity)
    for (code, name, year) in activity:
        data = {}
        data ["Name"] = name
        data ["Code"] = code
        data ["Year"] = year
        scraperwiki.datastore.save(["Name", "Year"], data, silent = True)
    print "Finished"

Main()



import urllib2
import re
import scraperwiki

START   = 2006
FINISH  = 2011

def GetActivity (start, finish):
    urlpat  = r"http://www.publications.parliament.uk/pa/ld20%02d%02d/ldhansrd/ldallfiles/peers/hansardbylord_atoz.htm"
    pat     = re.compile ('<a href="lord_hansard_(.*?)_home.html">(.*?), (.*?)</a>')
    activity= []
    for year in range (start, finish):
        y = year % 100
        url = urlpat % (y, y+1)
        html = scraperwiki.scrape (url)
        for m in pat.finditer (html):
            code = m.group (1)
            name = m.group (3) + " " + m.group(2)
            activity.append ((code, name, year))
    return activity

def Main():
    activity= GetActivity (START, FINISH)
    print len(activity)
    for (code, name, year) in activity:
        data = {}
        data ["Name"] = name
        data ["Code"] = code
        data ["Year"] = year
        scraperwiki.datastore.save(["Name", "Year"], data, silent = True)
    print "Finished"

Main()



