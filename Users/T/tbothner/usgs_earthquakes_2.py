import scraperwiki
import urllib
import lxml.html
import datetime
import re
import urlparse
import math

import dateutil.parser as parser

def stripstrong(td):
    if len(td) == 1 and td[0].tag == "strong":
        ttd = td[0]
        if len(ttd) == 1 and ttd[0].tag == "font":
            ttd = ttd[0]
    else:
        ttd = td
    assert len(ttd) == 0, lxml.html.tostring(td)
    return ttd.text
    

url = "http://earthquake.usgs.gov/earthquakes/recenteqsww/Quakes/quakes_all.html"
html = urllib.urlopen(url).read()
root = lxml.html.fromstring(html)
headers = ['', 'MAG', 'UTC DATE-TIMEy/m/d h:m:s', 'LATdeg', 'LONdeg', 'DEPTHkm', 'Region']
for table in root.cssselect("table"):
    ldata = [ ]
    rows = list(table)
    lheaders = [ th.text_content().strip()  for th in rows[0] ]
    assert lheaders == headers, (lheaders, headers)
    for row in rows[1:]:
        tds = list(row)
        data = { "LATdeg":float(tds[3].text.strip()), "LONdeg":float(tds[4].text.strip()), "DEPTHkm":float(tds[5].text.strip()) }
        data ['time'] = tds[2].text
        for el in tds[2]: 
            #print "TIME:", el.text
            isotime = parser.parse( el.text )
            print "ISO: ", isotime.isoformat()
            data ['datetime'] = isotime.isoformat()
        assert tds[2][0].tag == "a"
        href = tds[2][0].attrib.get("href")
        #print href
        data["link"] = urlparse.urljoin(url, href)
        mid = re.match("/earthquakes/recenteqsww/Quakes/(\w+).php", href)
        assert mid, href
        data["id"] = mid.group(1)
        data["MAG"] = float(stripstrong(tds[1]).strip())
        MAG = float(stripstrong(tds[1]).strip())
        Energy = float(math.pow(10, MAG))
        print "MAG=", MAG, "   Energy=", Energy
        data["Energy"] = Energy
        data["Region"] = stripstrong(tds[6]).strip()
        ldata.append(data)
    scraperwiki.sqlite.save(["id"], ldata)



import scraperwiki
import urllib
import lxml.html
import datetime
import re
import urlparse
import math

import dateutil.parser as parser

def stripstrong(td):
    if len(td) == 1 and td[0].tag == "strong":
        ttd = td[0]
        if len(ttd) == 1 and ttd[0].tag == "font":
            ttd = ttd[0]
    else:
        ttd = td
    assert len(ttd) == 0, lxml.html.tostring(td)
    return ttd.text
    

url = "http://earthquake.usgs.gov/earthquakes/recenteqsww/Quakes/quakes_all.html"
html = urllib.urlopen(url).read()
root = lxml.html.fromstring(html)
headers = ['', 'MAG', 'UTC DATE-TIMEy/m/d h:m:s', 'LATdeg', 'LONdeg', 'DEPTHkm', 'Region']
for table in root.cssselect("table"):
    ldata = [ ]
    rows = list(table)
    lheaders = [ th.text_content().strip()  for th in rows[0] ]
    assert lheaders == headers, (lheaders, headers)
    for row in rows[1:]:
        tds = list(row)
        data = { "LATdeg":float(tds[3].text.strip()), "LONdeg":float(tds[4].text.strip()), "DEPTHkm":float(tds[5].text.strip()) }
        data ['time'] = tds[2].text
        for el in tds[2]: 
            #print "TIME:", el.text
            isotime = parser.parse( el.text )
            print "ISO: ", isotime.isoformat()
            data ['datetime'] = isotime.isoformat()
        assert tds[2][0].tag == "a"
        href = tds[2][0].attrib.get("href")
        #print href
        data["link"] = urlparse.urljoin(url, href)
        mid = re.match("/earthquakes/recenteqsww/Quakes/(\w+).php", href)
        assert mid, href
        data["id"] = mid.group(1)
        data["MAG"] = float(stripstrong(tds[1]).strip())
        MAG = float(stripstrong(tds[1]).strip())
        Energy = float(math.pow(10, MAG))
        print "MAG=", MAG, "   Energy=", Energy
        data["Energy"] = Energy
        data["Region"] = stripstrong(tds[6]).strip()
        ldata.append(data)
    scraperwiki.sqlite.save(["id"], ldata)



