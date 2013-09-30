# scraping vienna air quality data
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

from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

wienerlufturlbase = "http://www.wien.gv.at/ma22-lgb/tb/"#tb20100501.htm"

def readAirData(dayurl):
    try:
        airdatahtml = urllib2.urlopen(dayurl).readlines()
    except urllib2.HTTPError, e:
        if e.code == 404:
            return
        raise e


    components = [ ]
    ndelimiters = 0
    airdata = { }
    for l in airdatahtml:
        mdelimiter = re.match("(-+?\+){8}", l)
        mdata7 = re.match("(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|", l)
        mdata8 = re.match("(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|", l)
        if mdelimiter:
            ndelimiters += 1 # delimiting line
            
        if mdata7 and mdata7.group(1).strip() == 'Messkomponente':
            # components measured
            for i in range(2,8):
                components.append(mdata7.group(i).strip())

        if mdata8:
            if ndelimiters == 2: # now reading data for each location
                assert components
                location = mdata8.group(1).strip()
                assert location not in airdata.keys()
                airdata[location] = { }
                j = 2
                for i in range(len(components)):
                    airdata[location][components[i]] = mdata8.group(j)
                    if components[i].find('Ozon') != -1:
                        j += 2
                    else:
                        j += 1
    return airdata
                    

def main(daysback):
    secsperday = 24 * 60 * 60
    yesterday = time.time() - secsperday
    for d in range(daysback)[::-1]:
        day = yesterday - d * secsperday
        daystring = time.strftime("%Y%m%d", time.gmtime(day))
        print daystring
        data = {'Date':daystring}
        dayurl = "%stb%s.htm" % (wienerlufturlbase, daystring)
        airdata = readAirData(dayurl)
        if airdata:
            data['PM10'] = int(airdata["WIEN - MITTEL"]['PM10'].strip())
            data['PM2c5'] = int(airdata["WIEN - MITTEL"]['PM2,5'].strip())
            data['CO max'] = float(airdata["WIEN - MITTEL"]['CO'].strip().split(' ')[-1])
            data['NO2'] = int(airdata["WIEN - MITTEL"]['NO2'].strip().split(' ')[-1])
            data['O3'] = int(airdata["WIEN - MITTEL"]['Ozon (O3)'].strip().split(' ')[-1])
            data['SO2'] = int(airdata["WIEN - MITTEL"]['SO2'].strip().split(' ')[-1])
            data['url'] = dayurl
            scraperwiki.sqlite.save(unique_keys=['Date'], data=data)
                                            
print "Starting... "
if 1:
    daydiff = datetime.date.today() - datetime.date(2012, 1, 27)
    daysback = daydiff.days
    daysback = 2 # reading 2 days back because the last day is only available at a later time, sometimes scraper runs early in morning before last day is online
    print 'Going back %d days' % daysback
    main(daysback)


#h = {"User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"}
#r = urllib2.Request("https://www.wien.gv.at/ma22-lgb/tb/tb20110201.htm")
#r.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')
#print r.headers
#print urllib2.urlopen(r).readlines()
#print urllib2.urlopen("http://www.wien.gv.at/ma22-lgb/tb/tb20110201.htm").readlines()



# scraping vienna air quality data
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

from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

wienerlufturlbase = "http://www.wien.gv.at/ma22-lgb/tb/"#tb20100501.htm"

def readAirData(dayurl):
    try:
        airdatahtml = urllib2.urlopen(dayurl).readlines()
    except urllib2.HTTPError, e:
        if e.code == 404:
            return
        raise e


    components = [ ]
    ndelimiters = 0
    airdata = { }
    for l in airdatahtml:
        mdelimiter = re.match("(-+?\+){8}", l)
        mdata7 = re.match("(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|", l)
        mdata8 = re.match("(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|", l)
        if mdelimiter:
            ndelimiters += 1 # delimiting line
            
        if mdata7 and mdata7.group(1).strip() == 'Messkomponente':
            # components measured
            for i in range(2,8):
                components.append(mdata7.group(i).strip())

        if mdata8:
            if ndelimiters == 2: # now reading data for each location
                assert components
                location = mdata8.group(1).strip()
                assert location not in airdata.keys()
                airdata[location] = { }
                j = 2
                for i in range(len(components)):
                    airdata[location][components[i]] = mdata8.group(j)
                    if components[i].find('Ozon') != -1:
                        j += 2
                    else:
                        j += 1
    return airdata
                    

def main(daysback):
    secsperday = 24 * 60 * 60
    yesterday = time.time() - secsperday
    for d in range(daysback)[::-1]:
        day = yesterday - d * secsperday
        daystring = time.strftime("%Y%m%d", time.gmtime(day))
        print daystring
        data = {'Date':daystring}
        dayurl = "%stb%s.htm" % (wienerlufturlbase, daystring)
        airdata = readAirData(dayurl)
        if airdata:
            data['PM10'] = int(airdata["WIEN - MITTEL"]['PM10'].strip())
            data['PM2c5'] = int(airdata["WIEN - MITTEL"]['PM2,5'].strip())
            data['CO max'] = float(airdata["WIEN - MITTEL"]['CO'].strip().split(' ')[-1])
            data['NO2'] = int(airdata["WIEN - MITTEL"]['NO2'].strip().split(' ')[-1])
            data['O3'] = int(airdata["WIEN - MITTEL"]['Ozon (O3)'].strip().split(' ')[-1])
            data['SO2'] = int(airdata["WIEN - MITTEL"]['SO2'].strip().split(' ')[-1])
            data['url'] = dayurl
            scraperwiki.sqlite.save(unique_keys=['Date'], data=data)
                                            
print "Starting... "
if 1:
    daydiff = datetime.date.today() - datetime.date(2012, 1, 27)
    daysback = daydiff.days
    daysback = 2 # reading 2 days back because the last day is only available at a later time, sometimes scraper runs early in morning before last day is online
    print 'Going back %d days' % daysback
    main(daysback)


#h = {"User-Agent": "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"}
#r = urllib2.Request("https://www.wien.gv.at/ma22-lgb/tb/tb20110201.htm")
#r.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')
#print r.headers
#print urllib2.urlopen(r).readlines()
#print urllib2.urlopen("http://www.wien.gv.at/ma22-lgb/tb/tb20110201.htm").readlines()



