# A big join in memory, just using sqlite, not datastore.

import random
import string
import time
import sqlite3 
import sys


conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute("create table t (id integer, val text)")
c.execute("insert into t (id, val) values (1, 'a')")
c.execute("insert into t (id, val) values (2, 'b')")
c.execute("insert into t (id, val) values (3, 'c')")
conn.commit()


print time.asctime()
for n in range(1,13):
    q = "select * from t " + ' '.join("join t as t%d" % i  for i in range(n))
    print q
    c.execute(q)
    print n, c, time.asctime()
    res = list(c)
    print len(res), sys.getsizeof(res), time.asctime()

# Haven't seen it get here
print "This script has finished"
# A big join in memory, just using sqlite, not datastore.

import random
import string
import time
import sqlite3 
import sys


conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute("create table t (id integer, val text)")
c.execute("insert into t (id, val) values (1, 'a')")
c.execute("insert into t (id, val) values (2, 'b')")
c.execute("insert into t (id, val) values (3, 'c')")
conn.commit()


print time.asctime()
for n in range(1,13):
    q = "select * from t " + ' '.join("join t as t%d" % i  for i in range(n))
    print q
    c.execute(q)
    print n, c, time.asctime()
    res = list(c)
    print len(res), sys.getsizeof(res), time.asctime()

# Haven't seen it get here
print "This script has finished"
