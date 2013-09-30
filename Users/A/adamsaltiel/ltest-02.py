import scraperwiki

scraperwiki.sqlite.execute("delete from swdata")
data = [ {"a":x*x}  for x in range(9) ]           
scraperwiki.sqlite.save(["a"], data)
print scraperwiki.sqlite.show_tables()
print scraperwiki.sqlite.execute("select * from swdata")
scraperwiki.sqlite.attach("ltest-01")
print scraperwiki.sqlite.select("* from 'ltest-01'.swdata limit 2")


import scraperwiki

scraperwiki.sqlite.execute("delete from swdata")
data = [ {"a":x*x}  for x in range(9) ]           
scraperwiki.sqlite.save(["a"], data)
print scraperwiki.sqlite.show_tables()
print scraperwiki.sqlite.execute("select * from swdata")
scraperwiki.sqlite.attach("ltest-01")
print scraperwiki.sqlite.select("* from 'ltest-01'.swdata limit 2")


