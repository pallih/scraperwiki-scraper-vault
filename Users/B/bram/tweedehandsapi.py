#import scraperwiki
#import urllib
#import json
# code ported from http://scraperwiki.com/views/python-api-access/

import urllib

try: import json
except: import simplejson as json

import scraperwiki

apiurl = "http://api.scraperwiki.com/api/1.0/"
#apiurl = "http://localhost:8010/api/1.0/"   # for local operation
apilimit = 500

attacheddata = [ ]
def getKeys(name):
    if name not in attacheddata:
        print "*** instead of getKeys('%s') please do\n    scraperwiki.sqlite.attach('%s') \n    print scraperwiki.sqlite.execute('select * from `%s`.swdata limit 0')['keys']" % (name, name, name)
        scraperwiki.sqlite.attach(name)
        attacheddata.append(name)
    result = scraperwiki.sqlite.execute("select * from `%s`.swdata limit 0" % name)
    if "error" in result:
        raise scraperwiki.sqlite.SqliteError(result["error"])
    return result["keys"]
    

def getData(name, limit=-1, offset=0):
    if name not in attacheddata:
        print "*** instead of getData('%s') please do\n    scraperwiki.sqlite.attach('%s') \n    print scraperwiki.sqlite.select('* from `%s`.swdata')" % (name, name, name)
        scraperwiki.sqlite.attach(name)
        attacheddata.append(name)
    
    count = 0
    loffset = 0
    while True:
        squery = [ "* from `%s`.swdata" % name ]
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
        squery.append("limit %d" % llimit)
        squery.append("offset %s" % (offset+loffset))
        lresult = scraperwiki.sqlite.select(" ".join(squery))
        for row in lresult:
            yield row
        count += len(lresult)
        if len(lresult) < llimit:  # run out of records
            break
        if limit != -1 and count >= limit:    # exceeded the limit
            break
        loffset += llimit


def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("getDataByDate has been deprecated")

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("getDataByLocation has been deprecated")
    
def search(name, filterdict, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("apiwrapper.search has been deprecated")



def getInfo(name, version=None, history_start_date=None, quietfields=None):
    query = {"name":name}
    if version:
        query["version"] = version
    if history_start_date:
        query["history_start_date"] = history_start_date
    if quietfields:
        query["quietfields"] = quietfields
    url = "%sscraper/getinfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def getRunInfo(name, runid=None):
    query = {"name":name}
    if runid:
        query["runid"] = runid
    url = "%sscraper/getruninfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def getUserInfo(username):
    query = {"username":username}
    url = "%sscraper/getuserinfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def scraperSearch(lquery):
    query = {"query":lquery}
    url = "%sscraper/search?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)
 


# Blank Python

# json container ? 
url = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=tweedehands&query=select%20*%20from%20%60tweedehands%60%20limit%2010'

vraag = urllib.urlopen(url).read()
print vraag 

#vraag = json.load(urllib2.Request("http//api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=imagetest&query=select%20*%20from%20swdata%20limit%2010"))
print type(json.loads(vraag))


result =  json.loads(vraag) 
# list of dictionary objects 
for ur in result:
#     print type(ur) # type ur  dictionary    type(url) str 
     print ur['fotoref']

# uitbreiding : in lokale   sql steken en dan in html pagina steken (jquery ? 
#  for teller1 in range(1 -- totaal/grootte pagina 
#  for teller2 in range(1 -- grootte pagina )

# pagina samenstellen   
#   schrijf   pagina head  teller 1  --- frame --- variabelen uit sql ----frameeinde ---pag  einde
#   haal beelden  op  -- nummering ?   

print result[1]['fotoref']
#import scraperwiki
#import urllib
#import json
# code ported from http://scraperwiki.com/views/python-api-access/

import urllib

try: import json
except: import simplejson as json

import scraperwiki

apiurl = "http://api.scraperwiki.com/api/1.0/"
#apiurl = "http://localhost:8010/api/1.0/"   # for local operation
apilimit = 500

attacheddata = [ ]
def getKeys(name):
    if name not in attacheddata:
        print "*** instead of getKeys('%s') please do\n    scraperwiki.sqlite.attach('%s') \n    print scraperwiki.sqlite.execute('select * from `%s`.swdata limit 0')['keys']" % (name, name, name)
        scraperwiki.sqlite.attach(name)
        attacheddata.append(name)
    result = scraperwiki.sqlite.execute("select * from `%s`.swdata limit 0" % name)
    if "error" in result:
        raise scraperwiki.sqlite.SqliteError(result["error"])
    return result["keys"]
    

def getData(name, limit=-1, offset=0):
    if name not in attacheddata:
        print "*** instead of getData('%s') please do\n    scraperwiki.sqlite.attach('%s') \n    print scraperwiki.sqlite.select('* from `%s`.swdata')" % (name, name, name)
        scraperwiki.sqlite.attach(name)
        attacheddata.append(name)
    
    count = 0
    loffset = 0
    while True:
        squery = [ "* from `%s`.swdata" % name ]
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
        squery.append("limit %d" % llimit)
        squery.append("offset %s" % (offset+loffset))
        lresult = scraperwiki.sqlite.select(" ".join(squery))
        for row in lresult:
            yield row
        count += len(lresult)
        if len(lresult) < llimit:  # run out of records
            break
        if limit != -1 and count >= limit:    # exceeded the limit
            break
        loffset += llimit


def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("getDataByDate has been deprecated")

def getDataByLocation(name, lat, lng, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("getDataByLocation has been deprecated")
    
def search(name, filterdict, limit=-1, offset=0):
    raise scraperwiki.sqlite.SqliteError("apiwrapper.search has been deprecated")



def getInfo(name, version=None, history_start_date=None, quietfields=None):
    query = {"name":name}
    if version:
        query["version"] = version
    if history_start_date:
        query["history_start_date"] = history_start_date
    if quietfields:
        query["quietfields"] = quietfields
    url = "%sscraper/getinfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def getRunInfo(name, runid=None):
    query = {"name":name}
    if runid:
        query["runid"] = runid
    url = "%sscraper/getruninfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def getUserInfo(username):
    query = {"username":username}
    url = "%sscraper/getuserinfo?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)

def scraperSearch(lquery):
    query = {"query":lquery}
    url = "%sscraper/search?%s" % (apiurl, urllib.urlencode(query))
    ljson = urllib.urlopen(url).read()
    return json.loads(ljson)
 


# Blank Python

# json container ? 
url = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=tweedehands&query=select%20*%20from%20%60tweedehands%60%20limit%2010'

vraag = urllib.urlopen(url).read()
print vraag 

#vraag = json.load(urllib2.Request("http//api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=imagetest&query=select%20*%20from%20swdata%20limit%2010"))
print type(json.loads(vraag))


result =  json.loads(vraag) 
# list of dictionary objects 
for ur in result:
#     print type(ur) # type ur  dictionary    type(url) str 
     print ur['fotoref']

# uitbreiding : in lokale   sql steken en dan in html pagina steken (jquery ? 
#  for teller1 in range(1 -- totaal/grootte pagina 
#  for teller2 in range(1 -- grootte pagina )

# pagina samenstellen   
#   schrijf   pagina head  teller 1  --- frame --- variabelen uit sql ----frameeinde ---pag  einde
#   haal beelden  op  -- nummering ?   

print result[1]['fotoref']
