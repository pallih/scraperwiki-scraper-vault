import scraperwiki

# Blank Python

print scraperwiki.sqlite.execute("create table if not exists jam (uid integer primary key, payload)")
print scraperwiki.sqlite.execute("begin transaction")
print scraperwiki.sqlite.execute("insert into jam values (4, 'random')")
print scraperwiki.sqlite.execute("rollback")
print scraperwiki.sqlite.select("* from jam")
import scraperwiki

# Blank Python

print scraperwiki.sqlite.execute("create table if not exists jam (uid integer primary key, payload)")
print scraperwiki.sqlite.execute("begin transaction")
print scraperwiki.sqlite.execute("insert into jam values (4, 'random')")
print scraperwiki.sqlite.execute("rollback")
print scraperwiki.sqlite.select("* from jam")
