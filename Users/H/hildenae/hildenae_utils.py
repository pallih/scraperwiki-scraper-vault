# -*- coding: UTF-8 -*-
import scraperwiki, urllib2, datetime, base64, time, re
from bs4 import BeautifulSoup
from collections import deque
import scraperwiki
import pprint # pretyyprint of records

def clearLocalCache(tableName='__cache'):
    try:
        scraperwiki.sqlite.execute("drop table %s;" % tableName)
    except scraperwiki.sqlite.SqliteError, e:
        if 'no such table: %s' % tableName not in str(e):
            raise e
        
def clearLazyCache():
    scraperwiki.sqlite.execute("drop table __lazycache;")

def removeDoubleSpaces(s):
    return " ".join(s.split()) #remove double spaces    

def findInCache(url,verbose=False, tableName='__cache'):
    try:
        r=scraperwiki.sqlite.select("* from %s where url=?" % tableName, url, verbose=0) # attempt grab from database.
    except scraperwiki.sqlite.SqliteError, e: # if table doesn't exist, don't bother checking
        if 'no such table: %s' % tableName in str(e):
            if verbose: print "Local: The cache table has not been created, please run putInCache once to create it" % e
            if verbose: print "Local: No cache match for '%s'" % url
        else:
            if verbose: print "Local: Warning (%s)" % e
        return None
    if len(r)>0:
        if verbose: print "Local: Cache match for '%s'" % url
        return base64.b64decode(r[0]['payload'])
    else:
        if verbose: print "Local: No cache match for '%s'" % url
        return None

def putInCache(url, xml,verbose=False, tableName='__cache'):
    scraperwiki.sqlite.save(table_name=tableName, data={'url':url,'payload':base64.b64encode(xml),'date':datetime.datetime.now()}, unique_keys=['url'], verbose=0)
    if verbose: print "Local: Put '%s' in cache" % url

def pretty(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

"""
UnicodeHexDump.py

Simple routine for dumping any kind of string, ascii, encoded, or 
unicode, to a standard hex dump.

Also two simple routines for reading and writing unicode strings
as encoded strings in a file.

Based on ASPN: Hex dumper -- Sebastien Keim & Raymond Hettinger 
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812 

Jack Trainor 2008
"""

""" dump any string to formatted hex output """
def dump(s):
    import types
    if type(s) == types.StringType:
        return dumpString(s)
    elif type(s) == types.UnicodeType:        
        return dumpUnicodeString(s)

FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])

""" dump any string, ascii or encoded, to formatted hex output """
def dumpString(src, length=16):
    result = []
    for i in xrange(0, len(src), length):
        chars = src[i:i+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        result.append("%04x  %-*s  %s\n" % (i, length*3, hex, printable))
    return ''.join(result)

""" dump unicode string to formatted hex output """
def dumpUnicodeString(src, length=8):
    result = []
    for i in xrange(0, len(src), length):
        unichars = src[i:i+length]
        hex = ' '.join(["%04x" % ord(x) for x in unichars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in unichars])
        result.append("%04x  %-*s  %s\n" % (i*2, length*5, hex, printable))
    return ''.join(result)

""" read unicode string from encoded file """
def readFile(path, encoding, errors="replace"):
    raw = open(path, 'rb').read()
    uniText = raw.decode(encoding, errors)
    return uniText

""" write unicode string to encoded file """
def writeFile(path, uniText, encoding, errors="replace"):
    encText = uniText.encode(encoding, errors)
    open(path, 'wb').write(encText)

if __name__ == 'scraper':
    import httplib
    httplib.HTTPConnection.debuglevel = 1                             
    import urllib2
    request = urllib2.Request('http://www.london2012.com/athletes/initial=E/index.html') 
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1')
    opener = urllib2.build_opener()                                   
    feeddata = opener.open(request).read() 
    print feeddata
    '''
    assert removeDoubleSpaces("Double  spaces       all  the  way") == "Double spaces all the way", "Not all double spaces removed"

    TESTTABLE='____test'
    TESTKEY='this can be any tag'
    TESTVALUE='and this can be any data'
    
    clearLocalCache(tableName=TESTTABLE)
    assert (findInCache(TESTKEY, verbose=True, tableName=TESTTABLE) == None), "Found data in empty cache"
    putInCache(TESTKEY, TESTVALUE,verbose=True, tableName=TESTTABLE)
    assert (findInCache(TESTKEY,verbose=True, tableName=TESTTABLE) == TESTVALUE) , "We found unknown data, or data was not inserted properly"
    clearLocalCache(tableName=TESTTABLE)
    assert (findInCache(TESTKEY,verbose=True, tableName=TESTTABLE) == None), "Table was not cleared properly"

    SOMESTRUCTURE = [[1, "Two"], 3, {True, False}, pretty]
    SOMESTRUCTURE[SOMESTRUCTURE[1]](SOMESTRUCTURE)

    TEST = u"Copyright: \u00a9\r\nRegistered: \u00ae\r\nAlpha: \u03b1\r\nOmega: \u03c9\r\n\Em dash: \u2015\r\n"
    
    print dump("ascii     " + TEST.encode("ascii", "replace"))
    print dump("Latin-1   " + TEST.encode("Latin-1", "replace"))
    print dump("utf8      " + TEST.encode("utf8", "replace"))
    print dump("utf16     " + TEST.encode("utf16", "replace"))
    print dump("utf-16-be " + TEST.encode("utf-16-be", "replace"))
    print dump("utf-16-le " + TEST.encode("utf-16-le", "replace"))
    print dump("unicode   " + TEST)
    
    #DELETE_ME_TXT = "deleteme.txt"
    #writeFile(DELETE_ME_TXT, TEST, "utf8")
    #uniText = readFile(DELETE_ME_TXT, "utf8")
    #assert (uniText == TEST)
    '''# -*- coding: UTF-8 -*-
import scraperwiki, urllib2, datetime, base64, time, re
from bs4 import BeautifulSoup
from collections import deque
import scraperwiki
import pprint # pretyyprint of records

def clearLocalCache(tableName='__cache'):
    try:
        scraperwiki.sqlite.execute("drop table %s;" % tableName)
    except scraperwiki.sqlite.SqliteError, e:
        if 'no such table: %s' % tableName not in str(e):
            raise e
        
def clearLazyCache():
    scraperwiki.sqlite.execute("drop table __lazycache;")

def removeDoubleSpaces(s):
    return " ".join(s.split()) #remove double spaces    

def findInCache(url,verbose=False, tableName='__cache'):
    try:
        r=scraperwiki.sqlite.select("* from %s where url=?" % tableName, url, verbose=0) # attempt grab from database.
    except scraperwiki.sqlite.SqliteError, e: # if table doesn't exist, don't bother checking
        if 'no such table: %s' % tableName in str(e):
            if verbose: print "Local: The cache table has not been created, please run putInCache once to create it" % e
            if verbose: print "Local: No cache match for '%s'" % url
        else:
            if verbose: print "Local: Warning (%s)" % e
        return None
    if len(r)>0:
        if verbose: print "Local: Cache match for '%s'" % url
        return base64.b64decode(r[0]['payload'])
    else:
        if verbose: print "Local: No cache match for '%s'" % url
        return None

def putInCache(url, xml,verbose=False, tableName='__cache'):
    scraperwiki.sqlite.save(table_name=tableName, data={'url':url,'payload':base64.b64encode(xml),'date':datetime.datetime.now()}, unique_keys=['url'], verbose=0)
    if verbose: print "Local: Put '%s' in cache" % url

def pretty(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

"""
UnicodeHexDump.py

Simple routine for dumping any kind of string, ascii, encoded, or 
unicode, to a standard hex dump.

Also two simple routines for reading and writing unicode strings
as encoded strings in a file.

Based on ASPN: Hex dumper -- Sebastien Keim & Raymond Hettinger 
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/142812 

Jack Trainor 2008
"""

""" dump any string to formatted hex output """
def dump(s):
    import types
    if type(s) == types.StringType:
        return dumpString(s)
    elif type(s) == types.UnicodeType:        
        return dumpUnicodeString(s)

FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])

""" dump any string, ascii or encoded, to formatted hex output """
def dumpString(src, length=16):
    result = []
    for i in xrange(0, len(src), length):
        chars = src[i:i+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        result.append("%04x  %-*s  %s\n" % (i, length*3, hex, printable))
    return ''.join(result)

""" dump unicode string to formatted hex output """
def dumpUnicodeString(src, length=8):
    result = []
    for i in xrange(0, len(src), length):
        unichars = src[i:i+length]
        hex = ' '.join(["%04x" % ord(x) for x in unichars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in unichars])
        result.append("%04x  %-*s  %s\n" % (i*2, length*5, hex, printable))
    return ''.join(result)

""" read unicode string from encoded file """
def readFile(path, encoding, errors="replace"):
    raw = open(path, 'rb').read()
    uniText = raw.decode(encoding, errors)
    return uniText

""" write unicode string to encoded file """
def writeFile(path, uniText, encoding, errors="replace"):
    encText = uniText.encode(encoding, errors)
    open(path, 'wb').write(encText)

if __name__ == 'scraper':
    import httplib
    httplib.HTTPConnection.debuglevel = 1                             
    import urllib2
    request = urllib2.Request('http://www.london2012.com/athletes/initial=E/index.html') 
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.60 Safari/537.1')
    opener = urllib2.build_opener()                                   
    feeddata = opener.open(request).read() 
    print feeddata
    '''
    assert removeDoubleSpaces("Double  spaces       all  the  way") == "Double spaces all the way", "Not all double spaces removed"

    TESTTABLE='____test'
    TESTKEY='this can be any tag'
    TESTVALUE='and this can be any data'
    
    clearLocalCache(tableName=TESTTABLE)
    assert (findInCache(TESTKEY, verbose=True, tableName=TESTTABLE) == None), "Found data in empty cache"
    putInCache(TESTKEY, TESTVALUE,verbose=True, tableName=TESTTABLE)
    assert (findInCache(TESTKEY,verbose=True, tableName=TESTTABLE) == TESTVALUE) , "We found unknown data, or data was not inserted properly"
    clearLocalCache(tableName=TESTTABLE)
    assert (findInCache(TESTKEY,verbose=True, tableName=TESTTABLE) == None), "Table was not cleared properly"

    SOMESTRUCTURE = [[1, "Two"], 3, {True, False}, pretty]
    SOMESTRUCTURE[SOMESTRUCTURE[1]](SOMESTRUCTURE)

    TEST = u"Copyright: \u00a9\r\nRegistered: \u00ae\r\nAlpha: \u03b1\r\nOmega: \u03c9\r\n\Em dash: \u2015\r\n"
    
    print dump("ascii     " + TEST.encode("ascii", "replace"))
    print dump("Latin-1   " + TEST.encode("Latin-1", "replace"))
    print dump("utf8      " + TEST.encode("utf8", "replace"))
    print dump("utf16     " + TEST.encode("utf16", "replace"))
    print dump("utf-16-be " + TEST.encode("utf-16-be", "replace"))
    print dump("utf-16-le " + TEST.encode("utf-16-le", "replace"))
    print dump("unicode   " + TEST)
    
    #DELETE_ME_TXT = "deleteme.txt"
    #writeFile(DELETE_ME_TXT, TEST, "utf8")
    #uniText = readFile(DELETE_ME_TXT, "utf8")
    #assert (uniText == TEST)
    '''