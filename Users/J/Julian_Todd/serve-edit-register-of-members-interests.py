import scraperwiki
from scraperwiki.datastore import sqlitecommand
import lxml.html
import urllib
import re
import os
import cgi
import json
import difflib
import datetime
import traceback
import sys


def MakeTables():
    mpchregfields = ["mpname text", "date text", "url", "contents text", "savedate text", "user text"]
    sqlitecommand("execute", "drop table if exists chregmemtext")
    sqlitecommand("execute", "create table chregmemtext (%s)" % ",".join(mpchregfields ))


monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 
             'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

categories = { 1:"directorships", 2:"employment", 3:"clients", 4:"sponsorships", 
               "4a":"campaign_sponsorships", "4b":"personal_sponsorships", 
               5:"gifts", 6:"oversea_trips", 7:"oversea_gifts", 8:"property", 
               9:"shares", 10:"transactions", 11:"miscellaneous", 12:"family" }


lineno = 0
def ParseCats(lines):
    if re.match("\s*Nil.", lines[0]):
        return {}
    global lineno
    cats = { }
    d = None
    for lineno, line in enumerate(lines):
        mheading = re.match("\*\*\s*(\d+)\.", line)
        if mheading:
            d = int(mheading.group(1))
            cats[d] = [ ]
        elif d != None:
            cats[d].append((lineno, line))
        else:
            assert not line.strip(), line
    return cats



def ParseDate(ds):
    md = re.match("(\d+)\s*([A-Z][a-z]+)\s*(\d+)$", ds.strip())
    assert md, ds
    return datetime.date(int(md.group(3)), monthdict[md.group(2)], int(md.group(1))).isoformat()
    
def ParseCat5(lines5):
    global lineno
    result = [ ]
    data = { }
    for lineno, line in lines5:
        if not line.strip():
            continue
        mregistered = re.match("\(Registered\s*(.*?)\)$", line.strip())
        if mregistered:
            data["regdate"] = ParseDate(mregistered.group(1))
            result.append(data)
            data = { }
            continue
        ic = line.find(":")
        key, value = line[:ic].strip(), line[ic+1:].strip()
        if key == "Name of donor":
            data["donorname"] = value
        if key == "Address of donor":
            data["donoraddress"] = value
        if key == "Date of receipt of donation":
            data["receptdate"] = ParseDate(value)
        if key == "Date of acceptance of donation":
            data["acceptdate"] = ParseDate(value)
        if key == "Donor status":
            data["donorstatus"] = value
    return result
    

sqlitecommand("attach", "scraperdownload_register_members_interests", "src")

def getrecenttext(mpname):
    r1 = sqlitecommand("execute", "select contents from regmemtext where mpname=?", (mpname,))
    r2 = sqlitecommand("execute", "select contents from chregmemtext where mpname=? order by savedate desc limit 1",
                           (mpname,))
    if r2["data"]:
        return r2["data"][0][0]
    return r1["data"][0][0]


def ParseErrs(contents):
    try:
        r = ParseCats(contents.split("\n"))
        r5 = ParseCat5(r.get(5, []))
        return {"data":r5}
    except ValueError, e:  pass
    except IndexError, e:  pass
    except AttributeError, e:  pass
    except AssertionError, e:  pass
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return { "err":str(e), "lineno":lineno, "trace":str(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)) }


qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
if not qs:
    print "missing"

elif "diff" in qs:
    contents = getrecenttext(qs["mpname"][0])
    contents = unicode(contents)
    econtents =(qs["contents"][0]).decode("latin1")
    d = difflib.Differ()
    c = d.compare(contents.split("\n"), econtents.split("\n"))
    a = list([e  for e in c  if e[:1] in ["+","-"]])
    print json.dumps({"back":a})

elif "save" in qs:
    pass

elif "contents" in qs:
    econtents =(qs["contents"][0]).decode("latin1")
    r = ParseCats(econtents.split("\n"))
    r5 = ParseCat5(r.get(5, []))
    print json.dumps({"back":[str(r5)]})

elif "list" in qs:
    result = sqlitecommand("execute", "select mpname from regmemtext limit 100")
    data = [ ]
    for ldata in result["data"]:
        mpname = ldata[0]
        contents = getrecenttext(mpname)
        pe = ParseErrs(contents)
        data.append([mpname, pe])
    print json.dumps(data)

elif "mpname" in qs:
    contents = getrecenttext(qs["mpname"][0])
    data = { }
    data["contents"] = contents.split("\n")
    pe = ParseErrs(contents)
    if "err" in pe:
        data.update(pe)
    print json.dumps(data)

else:
    print "nothing"


#MakeTables()
import scraperwiki
from scraperwiki.datastore import sqlitecommand
import lxml.html
import urllib
import re
import os
import cgi
import json
import difflib
import datetime
import traceback
import sys


def MakeTables():
    mpchregfields = ["mpname text", "date text", "url", "contents text", "savedate text", "user text"]
    sqlitecommand("execute", "drop table if exists chregmemtext")
    sqlitecommand("execute", "create table chregmemtext (%s)" % ",".join(mpchregfields ))


monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 
             'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

categories = { 1:"directorships", 2:"employment", 3:"clients", 4:"sponsorships", 
               "4a":"campaign_sponsorships", "4b":"personal_sponsorships", 
               5:"gifts", 6:"oversea_trips", 7:"oversea_gifts", 8:"property", 
               9:"shares", 10:"transactions", 11:"miscellaneous", 12:"family" }


lineno = 0
def ParseCats(lines):
    if re.match("\s*Nil.", lines[0]):
        return {}
    global lineno
    cats = { }
    d = None
    for lineno, line in enumerate(lines):
        mheading = re.match("\*\*\s*(\d+)\.", line)
        if mheading:
            d = int(mheading.group(1))
            cats[d] = [ ]
        elif d != None:
            cats[d].append((lineno, line))
        else:
            assert not line.strip(), line
    return cats



def ParseDate(ds):
    md = re.match("(\d+)\s*([A-Z][a-z]+)\s*(\d+)$", ds.strip())
    assert md, ds
    return datetime.date(int(md.group(3)), monthdict[md.group(2)], int(md.group(1))).isoformat()
    
def ParseCat5(lines5):
    global lineno
    result = [ ]
    data = { }
    for lineno, line in lines5:
        if not line.strip():
            continue
        mregistered = re.match("\(Registered\s*(.*?)\)$", line.strip())
        if mregistered:
            data["regdate"] = ParseDate(mregistered.group(1))
            result.append(data)
            data = { }
            continue
        ic = line.find(":")
        key, value = line[:ic].strip(), line[ic+1:].strip()
        if key == "Name of donor":
            data["donorname"] = value
        if key == "Address of donor":
            data["donoraddress"] = value
        if key == "Date of receipt of donation":
            data["receptdate"] = ParseDate(value)
        if key == "Date of acceptance of donation":
            data["acceptdate"] = ParseDate(value)
        if key == "Donor status":
            data["donorstatus"] = value
    return result
    

sqlitecommand("attach", "scraperdownload_register_members_interests", "src")

def getrecenttext(mpname):
    r1 = sqlitecommand("execute", "select contents from regmemtext where mpname=?", (mpname,))
    r2 = sqlitecommand("execute", "select contents from chregmemtext where mpname=? order by savedate desc limit 1",
                           (mpname,))
    if r2["data"]:
        return r2["data"][0][0]
    return r1["data"][0][0]


def ParseErrs(contents):
    try:
        r = ParseCats(contents.split("\n"))
        r5 = ParseCat5(r.get(5, []))
        return {"data":r5}
    except ValueError, e:  pass
    except IndexError, e:  pass
    except AttributeError, e:  pass
    except AssertionError, e:  pass
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return { "err":str(e), "lineno":lineno, "trace":str(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)) }


qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
if not qs:
    print "missing"

elif "diff" in qs:
    contents = getrecenttext(qs["mpname"][0])
    contents = unicode(contents)
    econtents =(qs["contents"][0]).decode("latin1")
    d = difflib.Differ()
    c = d.compare(contents.split("\n"), econtents.split("\n"))
    a = list([e  for e in c  if e[:1] in ["+","-"]])
    print json.dumps({"back":a})

elif "save" in qs:
    pass

elif "contents" in qs:
    econtents =(qs["contents"][0]).decode("latin1")
    r = ParseCats(econtents.split("\n"))
    r5 = ParseCat5(r.get(5, []))
    print json.dumps({"back":[str(r5)]})

elif "list" in qs:
    result = sqlitecommand("execute", "select mpname from regmemtext limit 100")
    data = [ ]
    for ldata in result["data"]:
        mpname = ldata[0]
        contents = getrecenttext(mpname)
        pe = ParseErrs(contents)
        data.append([mpname, pe])
    print json.dumps(data)

elif "mpname" in qs:
    contents = getrecenttext(qs["mpname"][0])
    data = { }
    data["contents"] = contents.split("\n")
    pe = ParseErrs(contents)
    if "err" in pe:
        data.update(pe)
    print json.dumps(data)

else:
    print "nothing"


#MakeTables()
import scraperwiki
from scraperwiki.datastore import sqlitecommand
import lxml.html
import urllib
import re
import os
import cgi
import json
import difflib
import datetime
import traceback
import sys


def MakeTables():
    mpchregfields = ["mpname text", "date text", "url", "contents text", "savedate text", "user text"]
    sqlitecommand("execute", "drop table if exists chregmemtext")
    sqlitecommand("execute", "create table chregmemtext (%s)" % ",".join(mpchregfields ))


monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 
             'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

categories = { 1:"directorships", 2:"employment", 3:"clients", 4:"sponsorships", 
               "4a":"campaign_sponsorships", "4b":"personal_sponsorships", 
               5:"gifts", 6:"oversea_trips", 7:"oversea_gifts", 8:"property", 
               9:"shares", 10:"transactions", 11:"miscellaneous", 12:"family" }


lineno = 0
def ParseCats(lines):
    if re.match("\s*Nil.", lines[0]):
        return {}
    global lineno
    cats = { }
    d = None
    for lineno, line in enumerate(lines):
        mheading = re.match("\*\*\s*(\d+)\.", line)
        if mheading:
            d = int(mheading.group(1))
            cats[d] = [ ]
        elif d != None:
            cats[d].append((lineno, line))
        else:
            assert not line.strip(), line
    return cats



def ParseDate(ds):
    md = re.match("(\d+)\s*([A-Z][a-z]+)\s*(\d+)$", ds.strip())
    assert md, ds
    return datetime.date(int(md.group(3)), monthdict[md.group(2)], int(md.group(1))).isoformat()
    
def ParseCat5(lines5):
    global lineno
    result = [ ]
    data = { }
    for lineno, line in lines5:
        if not line.strip():
            continue
        mregistered = re.match("\(Registered\s*(.*?)\)$", line.strip())
        if mregistered:
            data["regdate"] = ParseDate(mregistered.group(1))
            result.append(data)
            data = { }
            continue
        ic = line.find(":")
        key, value = line[:ic].strip(), line[ic+1:].strip()
        if key == "Name of donor":
            data["donorname"] = value
        if key == "Address of donor":
            data["donoraddress"] = value
        if key == "Date of receipt of donation":
            data["receptdate"] = ParseDate(value)
        if key == "Date of acceptance of donation":
            data["acceptdate"] = ParseDate(value)
        if key == "Donor status":
            data["donorstatus"] = value
    return result
    

sqlitecommand("attach", "scraperdownload_register_members_interests", "src")

def getrecenttext(mpname):
    r1 = sqlitecommand("execute", "select contents from regmemtext where mpname=?", (mpname,))
    r2 = sqlitecommand("execute", "select contents from chregmemtext where mpname=? order by savedate desc limit 1",
                           (mpname,))
    if r2["data"]:
        return r2["data"][0][0]
    return r1["data"][0][0]


def ParseErrs(contents):
    try:
        r = ParseCats(contents.split("\n"))
        r5 = ParseCat5(r.get(5, []))
        return {"data":r5}
    except ValueError, e:  pass
    except IndexError, e:  pass
    except AttributeError, e:  pass
    except AssertionError, e:  pass
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return { "err":str(e), "lineno":lineno, "trace":str(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)) }


qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
if not qs:
    print "missing"

elif "diff" in qs:
    contents = getrecenttext(qs["mpname"][0])
    contents = unicode(contents)
    econtents =(qs["contents"][0]).decode("latin1")
    d = difflib.Differ()
    c = d.compare(contents.split("\n"), econtents.split("\n"))
    a = list([e  for e in c  if e[:1] in ["+","-"]])
    print json.dumps({"back":a})

elif "save" in qs:
    pass

elif "contents" in qs:
    econtents =(qs["contents"][0]).decode("latin1")
    r = ParseCats(econtents.split("\n"))
    r5 = ParseCat5(r.get(5, []))
    print json.dumps({"back":[str(r5)]})

elif "list" in qs:
    result = sqlitecommand("execute", "select mpname from regmemtext limit 100")
    data = [ ]
    for ldata in result["data"]:
        mpname = ldata[0]
        contents = getrecenttext(mpname)
        pe = ParseErrs(contents)
        data.append([mpname, pe])
    print json.dumps(data)

elif "mpname" in qs:
    contents = getrecenttext(qs["mpname"][0])
    data = { }
    data["contents"] = contents.split("\n")
    pe = ParseErrs(contents)
    if "err" in pe:
        data.update(pe)
    print json.dumps(data)

else:
    print "nothing"


#MakeTables()
import scraperwiki
from scraperwiki.datastore import sqlitecommand
import lxml.html
import urllib
import re
import os
import cgi
import json
import difflib
import datetime
import traceback
import sys


def MakeTables():
    mpchregfields = ["mpname text", "date text", "url", "contents text", "savedate text", "user text"]
    sqlitecommand("execute", "drop table if exists chregmemtext")
    sqlitecommand("execute", "create table chregmemtext (%s)" % ",".join(mpchregfields ))


monthdict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 
             'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

categories = { 1:"directorships", 2:"employment", 3:"clients", 4:"sponsorships", 
               "4a":"campaign_sponsorships", "4b":"personal_sponsorships", 
               5:"gifts", 6:"oversea_trips", 7:"oversea_gifts", 8:"property", 
               9:"shares", 10:"transactions", 11:"miscellaneous", 12:"family" }


lineno = 0
def ParseCats(lines):
    if re.match("\s*Nil.", lines[0]):
        return {}
    global lineno
    cats = { }
    d = None
    for lineno, line in enumerate(lines):
        mheading = re.match("\*\*\s*(\d+)\.", line)
        if mheading:
            d = int(mheading.group(1))
            cats[d] = [ ]
        elif d != None:
            cats[d].append((lineno, line))
        else:
            assert not line.strip(), line
    return cats



def ParseDate(ds):
    md = re.match("(\d+)\s*([A-Z][a-z]+)\s*(\d+)$", ds.strip())
    assert md, ds
    return datetime.date(int(md.group(3)), monthdict[md.group(2)], int(md.group(1))).isoformat()
    
def ParseCat5(lines5):
    global lineno
    result = [ ]
    data = { }
    for lineno, line in lines5:
        if not line.strip():
            continue
        mregistered = re.match("\(Registered\s*(.*?)\)$", line.strip())
        if mregistered:
            data["regdate"] = ParseDate(mregistered.group(1))
            result.append(data)
            data = { }
            continue
        ic = line.find(":")
        key, value = line[:ic].strip(), line[ic+1:].strip()
        if key == "Name of donor":
            data["donorname"] = value
        if key == "Address of donor":
            data["donoraddress"] = value
        if key == "Date of receipt of donation":
            data["receptdate"] = ParseDate(value)
        if key == "Date of acceptance of donation":
            data["acceptdate"] = ParseDate(value)
        if key == "Donor status":
            data["donorstatus"] = value
    return result
    

sqlitecommand("attach", "scraperdownload_register_members_interests", "src")

def getrecenttext(mpname):
    r1 = sqlitecommand("execute", "select contents from regmemtext where mpname=?", (mpname,))
    r2 = sqlitecommand("execute", "select contents from chregmemtext where mpname=? order by savedate desc limit 1",
                           (mpname,))
    if r2["data"]:
        return r2["data"][0][0]
    return r1["data"][0][0]


def ParseErrs(contents):
    try:
        r = ParseCats(contents.split("\n"))
        r5 = ParseCat5(r.get(5, []))
        return {"data":r5}
    except ValueError, e:  pass
    except IndexError, e:  pass
    except AttributeError, e:  pass
    except AssertionError, e:  pass
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return { "err":str(e), "lineno":lineno, "trace":str(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)) }


qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
if not qs:
    print "missing"

elif "diff" in qs:
    contents = getrecenttext(qs["mpname"][0])
    contents = unicode(contents)
    econtents =(qs["contents"][0]).decode("latin1")
    d = difflib.Differ()
    c = d.compare(contents.split("\n"), econtents.split("\n"))
    a = list([e  for e in c  if e[:1] in ["+","-"]])
    print json.dumps({"back":a})

elif "save" in qs:
    pass

elif "contents" in qs:
    econtents =(qs["contents"][0]).decode("latin1")
    r = ParseCats(econtents.split("\n"))
    r5 = ParseCat5(r.get(5, []))
    print json.dumps({"back":[str(r5)]})

elif "list" in qs:
    result = sqlitecommand("execute", "select mpname from regmemtext limit 100")
    data = [ ]
    for ldata in result["data"]:
        mpname = ldata[0]
        contents = getrecenttext(mpname)
        pe = ParseErrs(contents)
        data.append([mpname, pe])
    print json.dumps(data)

elif "mpname" in qs:
    contents = getrecenttext(qs["mpname"][0])
    data = { }
    data["contents"] = contents.split("\n")
    pe = ParseErrs(contents)
    if "err" in pe:
        data.update(pe)
    print json.dumps(data)

else:
    print "nothing"


#MakeTables()
