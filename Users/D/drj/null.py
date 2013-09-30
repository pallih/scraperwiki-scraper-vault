import scraperwiki
import sqlite3

conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute("create table t (id integer, val text)")
c.execute("insert into t (id, val) values (1, 'a')")
c.execute("insert into t (id, val) values (2, X'bb00aa')")
c.execute(r"insert into t (id, val) values (3, 'c\x00seethis?')")
conn.commit()
c = conn.cursor()
l = list(c.execute("select * from t"))
print l
print repr(str(dict(l)[2]))import scraperwiki
import sqlite3

conn = sqlite3.connect(":memory:")
c = conn.cursor()
c.execute("create table t (id integer, val text)")
c.execute("insert into t (id, val) values (1, 'a')")
c.execute("insert into t (id, val) values (2, X'bb00aa')")
c.execute(r"insert into t (id, val) values (3, 'c\x00seethis?')")
conn.commit()
c = conn.cursor()
l = list(c.execute("select * from t"))
print l
print repr(str(dict(l)[2]))