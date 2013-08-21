import urllib2
import re
import scraperwiki

START   = 2006
FINISH  = 2012

def GetNames (start, finish):
    urlpat  = r"http://www.parliament.uk/mps-lords-and-offices/lords/"
    pat     = re.compile ('<a href="lord_hansard_(.*?)_home.html">(.*?), (.*?)</a>')
    lords = {}
    for year in range (start, finish):
        y = year % 100
        url = urlpat % (y, y+1)
        html = scraperwiki.scrape (url)
        for m in pat.finditer (html):
            code = m.group (1)
            name = m.group (3) + " " + m.group(2)
            if not code in lords:
                lords[code] = [name]
            lords[code].append (year)
    return lords

def Main():
    lords = GetNames (START, FINISH)
    for code in lords:
        data = {}
        data ["Name"] = lords[code][0]
        data ["Code"] = code
        for y in range (START,FINISH):
            yname = "%4d" % y
            if y in lords[code]:     
                data [yname] = 'Yes'
            else:
                data [yname] = 'No'
        scraperwiki.sqlite.save(["Name"], data)

Main()



