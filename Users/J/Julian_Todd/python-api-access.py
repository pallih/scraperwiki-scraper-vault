# code to be ported to scraperlibs once complete

import urllib

try: import json
except: import simplejson as json


apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500


def getKeys(name):
    url = "%sgetkeys?&name=%s" % (apiurl, name)
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)


def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % (apiurl, name, lat, lng)
    return generateData(urlbase, limit, offset)
    
def search(name, filterdict, limit=-1, offset=0):
    filter = "|".join(map(lambda x: "%s,%s" % (urllib.quote(x[0]), urllib.quote(x[1])), filterdict.items()))
    urlbase = "%ssearch?name=%s&filter=%s" % (apiurl, name, filter)
    return generateData(urlbase, limit, offset)


def Tests():
    global apilimit
    apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    for i, s in enumerate(getData(name1, limit=110)):
        print i, s
        
    print "get data by date"
    for i, s in enumerate(getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12")):
        print i, s

    print "get data by location"
    for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
        print i, s
    
    print "search test"
    filterdict = {'Distributing_Body': 'UK Sport', "Region":"London"}
    for i, s in enumerate(search(name2, filterdict, offset=5, limit=17)):
        print i, s
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
    print i, s
# code to be ported to scraperlibs once complete

import urllib

try: import json
except: import simplejson as json


apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500


def getKeys(name):
    url = "%sgetkeys?&name=%s" % (apiurl, name)
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)


def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % (apiurl, name, lat, lng)
    return generateData(urlbase, limit, offset)
    
def search(name, filterdict, limit=-1, offset=0):
    filter = "|".join(map(lambda x: "%s,%s" % (urllib.quote(x[0]), urllib.quote(x[1])), filterdict.items()))
    urlbase = "%ssearch?name=%s&filter=%s" % (apiurl, name, filter)
    return generateData(urlbase, limit, offset)


def Tests():
    global apilimit
    apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    for i, s in enumerate(getData(name1, limit=110)):
        print i, s
        
    print "get data by date"
    for i, s in enumerate(getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12")):
        print i, s

    print "get data by location"
    for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
        print i, s
    
    print "search test"
    filterdict = {'Distributing_Body': 'UK Sport', "Region":"London"}
    for i, s in enumerate(search(name2, filterdict, offset=5, limit=17)):
        print i, s
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
    print i, s
# code to be ported to scraperlibs once complete

import urllib

try: import json
except: import simplejson as json


apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500


def getKeys(name):
    url = "%sgetkeys?&name=%s" % (apiurl, name)
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)


def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % (apiurl, name, lat, lng)
    return generateData(urlbase, limit, offset)
    
def search(name, filterdict, limit=-1, offset=0):
    filter = "|".join(map(lambda x: "%s,%s" % (urllib.quote(x[0]), urllib.quote(x[1])), filterdict.items()))
    urlbase = "%ssearch?name=%s&filter=%s" % (apiurl, name, filter)
    return generateData(urlbase, limit, offset)


def Tests():
    global apilimit
    apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    for i, s in enumerate(getData(name1, limit=110)):
        print i, s
        
    print "get data by date"
    for i, s in enumerate(getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12")):
        print i, s

    print "get data by location"
    for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
        print i, s
    
    print "search test"
    filterdict = {'Distributing_Body': 'UK Sport', "Region":"London"}
    for i, s in enumerate(search(name2, filterdict, offset=5, limit=17)):
        print i, s
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
    print i, s
# code to be ported to scraperlibs once complete

import urllib

try: import json
except: import simplejson as json


apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500


def getKeys(name):
    url = "%sgetkeys?&name=%s" % (apiurl, name)
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)


def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % (apiurl, name, lat, lng)
    return generateData(urlbase, limit, offset)
    
def search(name, filterdict, limit=-1, offset=0):
    filter = "|".join(map(lambda x: "%s,%s" % (urllib.quote(x[0]), urllib.quote(x[1])), filterdict.items()))
    urlbase = "%ssearch?name=%s&filter=%s" % (apiurl, name, filter)
    return generateData(urlbase, limit, offset)


def Tests():
    global apilimit
    apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    for i, s in enumerate(getData(name1, limit=110)):
        print i, s
        
    print "get data by date"
    for i, s in enumerate(getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12")):
        print i, s

    print "get data by location"
    for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
        print i, s
    
    print "search test"
    filterdict = {'Distributing_Body': 'UK Sport', "Region":"London"}
    for i, s in enumerate(search(name2, filterdict, offset=5, limit=17)):
        print i, s
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
    print i, s
# code to be ported to scraperlibs once complete

import urllib

try: import json
except: import simplejson as json


apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500


def getKeys(name):
    url = "%sgetkeys?&name=%s" % (apiurl, name)
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)


def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    urlbase = "%sgetdatabylocation?name=%s&lat=%f&lng=%f" % (apiurl, name, lat, lng)
    return generateData(urlbase, limit, offset)
    
def search(name, filterdict, limit=-1, offset=0):
    filter = "|".join(map(lambda x: "%s,%s" % (urllib.quote(x[0]), urllib.quote(x[1])), filterdict.items()))
    urlbase = "%ssearch?name=%s&filter=%s" % (apiurl, name, filter)
    return generateData(urlbase, limit, offset)


def Tests():
    global apilimit
    apilimit = 50  # easier to test

    name1 = "uk-offshore-oil-wells"
    name2 = "uk-lottery-grants"
    
    print getKeys(name1)
    
    for i, s in enumerate(getData(name1, limit=110)):
        print i, s
        
    print "get data by date"
    for i, s in enumerate(getDataByDate(name2, start_date="2009-01-01", end_date="2009-01-12")):
        print i, s

    print "get data by location"
    for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
        print i, s
    
    print "search test"
    filterdict = {'Distributing_Body': 'UK Sport', "Region":"London"}
    for i, s in enumerate(search(name2, filterdict, offset=5, limit=17)):
        print i, s
        
#Tests()
name1 = "uk-offshore-oil-wells"
for i, s in enumerate(getDataByLocation(name1, lat=59.033358, lng=1.0486569, limit=60)):
    print i, s
