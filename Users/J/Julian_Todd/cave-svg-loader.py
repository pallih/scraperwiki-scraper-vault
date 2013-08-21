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


