import sqlite3
import scraperwiki

import urllib
import tempfile
import simplejson as json
import scraperwiki
import re
import os

# code which effectively imports another sqlite database

url = "http://seagrass.goatchurch.org.uk/~julian/rumblingmain2010-sketch.sqlite"
if os.getenv("URLQUERY") == "ireby":
    url = "http://seagrass.goatchurch.org.uk/~julian/Ireby-2010-11-14.sqlite"

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen(url).read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

c.execute("SELECT * from sqlite_master")
tables = list(c)
for table in tables:
    if not table[4]:
        continue
    scraperwiki.sqlite.execute("drop table if exists `%s`" % table[1])
    scraperwiki.sqlite.execute(table[4])
    c.execute("select * from `%s`" % table[1])
    for v in c:
        cmd = "insert into `%s` values (%s)" % (table[1], ",".join(["?"]*len(v)))
        scraperwiki.sqlite.execute(cmd, v, verbose=0)
    scraperwiki.sqlite.commit()





def parsestyle(sdef):
    return dict(re.findall('([\w\-]*)\s*:\s*([^;]*?)[;$]', sdef))

def Main():
    data = { }

    #pathid integer unique, linestyle text, d text, bsplined boolean, pathidtailleft integer, 
    #btailleftfore boolean, pathidheadright integer, bheadrightfore boolean, zalttail real, zalthead real
    c.execute("SELECT * from paths limit 5000")
    keys = [ k[0]  for k in c.description ]
    data["paths"] = [ dict(zip(keys, v))  for v in c ]

    #pathid integer, sfsketch text, scaledown real, rotatedeg real, xtrans real, ytrans real, submapping text, style text
    c.execute("SELECT * from sketchframes where imagepixelswidth>0 limit 50")
    keys = [ k[0]  for k in c.description ]
    data["sketchframes"] = [ dict(zip(keys, v))  for v in c ]

    print json.dumps(data)

#Main()
import sqlite3
import scraperwiki

import urllib
import tempfile
import simplejson as json
import scraperwiki
import re
import os

# code which effectively imports another sqlite database

url = "http://seagrass.goatchurch.org.uk/~julian/rumblingmain2010-sketch.sqlite"
if os.getenv("URLQUERY") == "ireby":
    url = "http://seagrass.goatchurch.org.uk/~julian/Ireby-2010-11-14.sqlite"

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen(url).read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

c.execute("SELECT * from sqlite_master")
tables = list(c)
for table in tables:
    if not table[4]:
        continue
    scraperwiki.sqlite.execute("drop table if exists `%s`" % table[1])
    scraperwiki.sqlite.execute(table[4])
    c.execute("select * from `%s`" % table[1])
    for v in c:
        cmd = "insert into `%s` values (%s)" % (table[1], ",".join(["?"]*len(v)))
        scraperwiki.sqlite.execute(cmd, v, verbose=0)
    scraperwiki.sqlite.commit()





def parsestyle(sdef):
    return dict(re.findall('([\w\-]*)\s*:\s*([^;]*?)[;$]', sdef))

def Main():
    data = { }

    #pathid integer unique, linestyle text, d text, bsplined boolean, pathidtailleft integer, 
    #btailleftfore boolean, pathidheadright integer, bheadrightfore boolean, zalttail real, zalthead real
    c.execute("SELECT * from paths limit 5000")
    keys = [ k[0]  for k in c.description ]
    data["paths"] = [ dict(zip(keys, v))  for v in c ]

    #pathid integer, sfsketch text, scaledown real, rotatedeg real, xtrans real, ytrans real, submapping text, style text
    c.execute("SELECT * from sketchframes where imagepixelswidth>0 limit 50")
    keys = [ k[0]  for k in c.description ]
    data["sketchframes"] = [ dict(zip(keys, v))  for v in c ]

    print json.dumps(data)

#Main()
import sqlite3
import scraperwiki

import urllib
import tempfile
import simplejson as json
import scraperwiki
import re
import os

# code which effectively imports another sqlite database

url = "http://seagrass.goatchurch.org.uk/~julian/rumblingmain2010-sketch.sqlite"
if os.getenv("URLQUERY") == "ireby":
    url = "http://seagrass.goatchurch.org.uk/~julian/Ireby-2010-11-14.sqlite"

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen(url).read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

c.execute("SELECT * from sqlite_master")
tables = list(c)
for table in tables:
    if not table[4]:
        continue
    scraperwiki.sqlite.execute("drop table if exists `%s`" % table[1])
    scraperwiki.sqlite.execute(table[4])
    c.execute("select * from `%s`" % table[1])
    for v in c:
        cmd = "insert into `%s` values (%s)" % (table[1], ",".join(["?"]*len(v)))
        scraperwiki.sqlite.execute(cmd, v, verbose=0)
    scraperwiki.sqlite.commit()





def parsestyle(sdef):
    return dict(re.findall('([\w\-]*)\s*:\s*([^;]*?)[;$]', sdef))

def Main():
    data = { }

    #pathid integer unique, linestyle text, d text, bsplined boolean, pathidtailleft integer, 
    #btailleftfore boolean, pathidheadright integer, bheadrightfore boolean, zalttail real, zalthead real
    c.execute("SELECT * from paths limit 5000")
    keys = [ k[0]  for k in c.description ]
    data["paths"] = [ dict(zip(keys, v))  for v in c ]

    #pathid integer, sfsketch text, scaledown real, rotatedeg real, xtrans real, ytrans real, submapping text, style text
    c.execute("SELECT * from sketchframes where imagepixelswidth>0 limit 50")
    keys = [ k[0]  for k in c.description ]
    data["sketchframes"] = [ dict(zip(keys, v))  for v in c ]

    print json.dumps(data)

#Main()
import sqlite3
import scraperwiki

import urllib
import tempfile
import simplejson as json
import scraperwiki
import re
import os

# code which effectively imports another sqlite database

url = "http://seagrass.goatchurch.org.uk/~julian/rumblingmain2010-sketch.sqlite"
if os.getenv("URLQUERY") == "ireby":
    url = "http://seagrass.goatchurch.org.uk/~julian/Ireby-2010-11-14.sqlite"

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen(url).read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

c.execute("SELECT * from sqlite_master")
tables = list(c)
for table in tables:
    if not table[4]:
        continue
    scraperwiki.sqlite.execute("drop table if exists `%s`" % table[1])
    scraperwiki.sqlite.execute(table[4])
    c.execute("select * from `%s`" % table[1])
    for v in c:
        cmd = "insert into `%s` values (%s)" % (table[1], ",".join(["?"]*len(v)))
        scraperwiki.sqlite.execute(cmd, v, verbose=0)
    scraperwiki.sqlite.commit()





def parsestyle(sdef):
    return dict(re.findall('([\w\-]*)\s*:\s*([^;]*?)[;$]', sdef))

def Main():
    data = { }

    #pathid integer unique, linestyle text, d text, bsplined boolean, pathidtailleft integer, 
    #btailleftfore boolean, pathidheadright integer, bheadrightfore boolean, zalttail real, zalthead real
    c.execute("SELECT * from paths limit 5000")
    keys = [ k[0]  for k in c.description ]
    data["paths"] = [ dict(zip(keys, v))  for v in c ]

    #pathid integer, sfsketch text, scaledown real, rotatedeg real, xtrans real, ytrans real, submapping text, style text
    c.execute("SELECT * from sketchframes where imagepixelswidth>0 limit 50")
    keys = [ k[0]  for k in c.description ]
    data["sketchframes"] = [ dict(zip(keys, v))  for v in c ]

    print json.dumps(data)

#Main()
import sqlite3
import scraperwiki

import urllib
import tempfile
import simplejson as json
import scraperwiki
import re
import os

# code which effectively imports another sqlite database

url = "http://seagrass.goatchurch.org.uk/~julian/rumblingmain2010-sketch.sqlite"
if os.getenv("URLQUERY") == "ireby":
    url = "http://seagrass.goatchurch.org.uk/~julian/Ireby-2010-11-14.sqlite"

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen(url).read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

c.execute("SELECT * from sqlite_master")
tables = list(c)
for table in tables:
    if not table[4]:
        continue
    scraperwiki.sqlite.execute("drop table if exists `%s`" % table[1])
    scraperwiki.sqlite.execute(table[4])
    c.execute("select * from `%s`" % table[1])
    for v in c:
        cmd = "insert into `%s` values (%s)" % (table[1], ",".join(["?"]*len(v)))
        scraperwiki.sqlite.execute(cmd, v, verbose=0)
    scraperwiki.sqlite.commit()





def parsestyle(sdef):
    return dict(re.findall('([\w\-]*)\s*:\s*([^;]*?)[;$]', sdef))

def Main():
    data = { }

    #pathid integer unique, linestyle text, d text, bsplined boolean, pathidtailleft integer, 
    #btailleftfore boolean, pathidheadright integer, bheadrightfore boolean, zalttail real, zalthead real
    c.execute("SELECT * from paths limit 5000")
    keys = [ k[0]  for k in c.description ]
    data["paths"] = [ dict(zip(keys, v))  for v in c ]

    #pathid integer, sfsketch text, scaledown real, rotatedeg real, xtrans real, ytrans real, submapping text, style text
    c.execute("SELECT * from sketchframes where imagepixelswidth>0 limit 50")
    keys = [ k[0]  for k in c.description ]
    data["sketchframes"] = [ dict(zip(keys, v))  for v in c ]

    print json.dumps(data)

#Main()
