# sadly merseytravel seem to have changed their website, and I can't find a link to list stations on the network anymore.
# so for now I have taken the scraper out of scheduling...

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import urllib
import re
import urlparse

def GetLatLng(postcode):
    url = "http://maps.google.co.uk/maps/geo?output=csv&" + urllib.urlencode({"q": postcode})
    r = urllib2.urlopen(url).read()
    rl = r.split(",")
    return (rl[2], rl[3])




#<dt class="clear">Car park spaces</dt>
#                                        <dd class="clear">61</dd>


def readstationnames():
    stations = [ ]
    for i in range(1, 20):
        url = "http://www.merseytravel.gov.uk/agsearch.asp?FormMode=Search&transporttypeID=1&page=%d&keyword=&borough=0" % i
        html = urllib2.urlopen(url).read()
        stats = re.findall('<li><a href="(rview.asp.*?)">\s*(.*?)\s*</a></li>', html)
        for link, station in stats:
            urlstat = urlparse.urljoin(url, re.sub("&amp;", "&", link))
            stations.append((station, urlstat))
            #print station, urlstat
        
    return stations

def getNatRailStationInfo(s):
    url = "http://www.nationalrail.co.uk/stations_destinations/"
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name="findStationForm")
    br['stnq'] = s
    response = br.submit()
    r = response.read()
    return r

def stationPostcode(r):
    adr = re.findall("<address>.*</address>", r, re.DOTALL)
    if len(adr) == 1:
        a = adr[0]
        adrlines = [f.strip() for f in a.split("\n")]
        postcode = adrlines[-2]
        print postcode
        return postcode

def scrapestation(s, urlstat):
    data = {}
    # new url to get address from nationalrail
    r = getNatRailStationInfo(s)
    pc = stationPostcode(r)
    if not pc:
        r = getNatRailStationInfo("%s (Merseyside)" % s)
        pc = stationPostcode(r)


    data["station name"] = s
    data["station url"] = urlstat
    data["postcode"] = pc
    if s == 'Liverpool Moorfields':
        data["postcode"] = 'L2 2BS'

    # find car park spaces
    cps = re.match('.*<dt class=".*?">Car park spaces</dt>\s*\n\s*<dd class=".*?">(.*?)</dd>', r, re.DOTALL)
    data["Car park spaces"] = ""
    if cps:
        data["Car park spaces"] = cps.group(1).strip()

    # wheelchair access
    wca = re.match('.*<dt class=".*?">Wheelchairs</dt>\s*\n\s*<dd class=".*?">.*?\/>(.*?)</dd>', r, re.DOTALL)
    data["Wheelchairs"] = ""
    if wca:
         data["Wheelchairs"] = wca.group(1).strip()

    # cycle parking (would be on merseyrail site)

    #cpa = re.match('.*<dt class="clear">Wheelchairs</dt>\s*\n\s*<dd class="clear">(.*?)</dd>', r, re.DOTALL)
    cpahtml = urllib.urlopen(urlstat).read()
    cpa1 = re.match(".*\n<li>([0-9]+)\s*[Cc]ycles", cpahtml, re.DOTALL)
    cpa2 = re.match(".*([0-9]+)\s*[Cc]ycle [Pp]arking", cpahtml, re.DOTALL)
    cpa3 = re.match(".*([0-9]+)\s*[Bb]ike [Rr]ac?ks?", cpahtml, re.DOTALL)
    data["Cycle park spaces"] = "Unknown"
    if cpa1:
        data["Cycle park spaces"] = cpa1.group(1).strip()
    elif cpa2:
        data["Cycle park spaces"] = cpa2.group(1).strip()
    elif cpa3:
        data["Cycle park spaces"] = cpa3.group(1).strip()

    # lines
    lines = re.match('.*<dd>.*<strong>Lines:</strong>(.*?)</dd>', cpahtml, re.DOTALL)
    data["Lines"] = ""
    if lines:
         data["Lines"] = lines.group(1).strip()
    
    data["Code"] = getStationCode(data["postcode"])
        
    if data["postcode"]:
        #data["latlng"] = scraperwiki.geo.gb_postcode_to_latlng(data["postcode"])
        data["latlng"] = GetLatLng(data["postcode"])
        scraperwiki.sqlite.save(unique_keys=["station name"], data=data)
    else:
        scraperwiki.sqlite.save(unique_keys=["station name"], data=data)

def getStationCode(postcode):
    records = scraperwiki.sqlite.select("code FROM all_stations_list.swdata WHERE postcode = '%s'" % postcode)
    if len(records) == 0:
        return None
    return records[0]['code']

def main():
    stations = readstationnames()
    for s, urlstat in stations:
        scrapestation(s, urlstat)

                
print "Starting... "
scraperwiki.sqlite.attach('list_of_uk_railway_station_locations', 'all_stations_list')
#latlng = GetLatLng("L8 2UW")
#print "%f %f" % (latlng[0], latlng[1])
#scrapestation("West Allerton", "http://www.merseytravel.gov.uk/rview.asp?id=38&transporttypeID=1")
#print getStationCode("Liverpool Central")
main()

# sadly merseytravel seem to have changed their website, and I can't find a link to list stations on the network anymore.
# so for now I have taken the scraper out of scheduling...

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import urllib
import re
import urlparse

def GetLatLng(postcode):
    url = "http://maps.google.co.uk/maps/geo?output=csv&" + urllib.urlencode({"q": postcode})
    r = urllib2.urlopen(url).read()
    rl = r.split(",")
    return (rl[2], rl[3])




#<dt class="clear">Car park spaces</dt>
#                                        <dd class="clear">61</dd>


def readstationnames():
    stations = [ ]
    for i in range(1, 20):
        url = "http://www.merseytravel.gov.uk/agsearch.asp?FormMode=Search&transporttypeID=1&page=%d&keyword=&borough=0" % i
        html = urllib2.urlopen(url).read()
        stats = re.findall('<li><a href="(rview.asp.*?)">\s*(.*?)\s*</a></li>', html)
        for link, station in stats:
            urlstat = urlparse.urljoin(url, re.sub("&amp;", "&", link))
            stations.append((station, urlstat))
            #print station, urlstat
        
    return stations

def getNatRailStationInfo(s):
    url = "http://www.nationalrail.co.uk/stations_destinations/"
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name="findStationForm")
    br['stnq'] = s
    response = br.submit()
    r = response.read()
    return r

def stationPostcode(r):
    adr = re.findall("<address>.*</address>", r, re.DOTALL)
    if len(adr) == 1:
        a = adr[0]
        adrlines = [f.strip() for f in a.split("\n")]
        postcode = adrlines[-2]
        print postcode
        return postcode

def scrapestation(s, urlstat):
    data = {}
    # new url to get address from nationalrail
    r = getNatRailStationInfo(s)
    pc = stationPostcode(r)
    if not pc:
        r = getNatRailStationInfo("%s (Merseyside)" % s)
        pc = stationPostcode(r)


    data["station name"] = s
    data["station url"] = urlstat
    data["postcode"] = pc
    if s == 'Liverpool Moorfields':
        data["postcode"] = 'L2 2BS'

    # find car park spaces
    cps = re.match('.*<dt class=".*?">Car park spaces</dt>\s*\n\s*<dd class=".*?">(.*?)</dd>', r, re.DOTALL)
    data["Car park spaces"] = ""
    if cps:
        data["Car park spaces"] = cps.group(1).strip()

    # wheelchair access
    wca = re.match('.*<dt class=".*?">Wheelchairs</dt>\s*\n\s*<dd class=".*?">.*?\/>(.*?)</dd>', r, re.DOTALL)
    data["Wheelchairs"] = ""
    if wca:
         data["Wheelchairs"] = wca.group(1).strip()

    # cycle parking (would be on merseyrail site)

    #cpa = re.match('.*<dt class="clear">Wheelchairs</dt>\s*\n\s*<dd class="clear">(.*?)</dd>', r, re.DOTALL)
    cpahtml = urllib.urlopen(urlstat).read()
    cpa1 = re.match(".*\n<li>([0-9]+)\s*[Cc]ycles", cpahtml, re.DOTALL)
    cpa2 = re.match(".*([0-9]+)\s*[Cc]ycle [Pp]arking", cpahtml, re.DOTALL)
    cpa3 = re.match(".*([0-9]+)\s*[Bb]ike [Rr]ac?ks?", cpahtml, re.DOTALL)
    data["Cycle park spaces"] = "Unknown"
    if cpa1:
        data["Cycle park spaces"] = cpa1.group(1).strip()
    elif cpa2:
        data["Cycle park spaces"] = cpa2.group(1).strip()
    elif cpa3:
        data["Cycle park spaces"] = cpa3.group(1).strip()

    # lines
    lines = re.match('.*<dd>.*<strong>Lines:</strong>(.*?)</dd>', cpahtml, re.DOTALL)
    data["Lines"] = ""
    if lines:
         data["Lines"] = lines.group(1).strip()
    
    data["Code"] = getStationCode(data["postcode"])
        
    if data["postcode"]:
        #data["latlng"] = scraperwiki.geo.gb_postcode_to_latlng(data["postcode"])
        data["latlng"] = GetLatLng(data["postcode"])
        scraperwiki.sqlite.save(unique_keys=["station name"], data=data)
    else:
        scraperwiki.sqlite.save(unique_keys=["station name"], data=data)

def getStationCode(postcode):
    records = scraperwiki.sqlite.select("code FROM all_stations_list.swdata WHERE postcode = '%s'" % postcode)
    if len(records) == 0:
        return None
    return records[0]['code']

def main():
    stations = readstationnames()
    for s, urlstat in stations:
        scrapestation(s, urlstat)

                
print "Starting... "
scraperwiki.sqlite.attach('list_of_uk_railway_station_locations', 'all_stations_list')
#latlng = GetLatLng("L8 2UW")
#print "%f %f" % (latlng[0], latlng[1])
#scrapestation("West Allerton", "http://www.merseytravel.gov.uk/rview.asp?id=38&transporttypeID=1")
#print getStationCode("Liverpool Central")
main()

