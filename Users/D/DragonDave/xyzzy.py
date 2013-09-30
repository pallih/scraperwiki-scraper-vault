import scraperwiki
import datetime
# Blank Python

d = datetime.date.today()
scraperwiki.sqlite.save_var('jam',d)
dd = scraperwiki.sqlite.get_var('jam')
print dd
print type(dd)

print d
import scraperwiki
import datetime
# Blank Python

d = datetime.date.today()
scraperwiki.sqlite.save_var('jam',d)
dd = scraperwiki.sqlite.get_var('jam')
print dd
print type(dd)

print d
